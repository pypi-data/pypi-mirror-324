import asyncio
import os
import ssl
import threading
import warnings
from functools import wraps
from http import HTTPStatus
from typing import Optional, Union
from urllib.parse import urlparse

import aiohttp
import nest_asyncio
import requests
from pydantic import BaseModel

from bigdata_client.clerk.constants import ClerkInstanceType
from bigdata_client.clerk.exceptions import (
    ClerkAuthError,
    ClerkAuthUnsupportedError,
    ClerkInvalidCredentialsError,
    ClerkTooManySignInAttemptsError,
    ClerkUnexpectedSignInParametersError,
)
from bigdata_client.clerk.models import SignInStrategyType
from bigdata_client.clerk.token_manager import ClerkTokenManager
from bigdata_client.clerk.token_manager_factory import token_manager_factory
from bigdata_client.constants import DEPRECATED_WARNING_AUTOSUGGEST
from bigdata_client.exceptions import (
    BigdataClientAuthFlowError,
    BigdataClientError,
    BigdataClientTooManySignInAttemptsError,
)
from bigdata_client.settings import settings
from bigdata_client.user_agent import get_user_agent

nest_asyncio.apply()  # Required for running asyncio in notebooks
THREAD_WAIT_TIMEOUT = 100


class AsyncRequestContext(BaseModel):
    """
    Context used to pass information to auth module for making async requests.
    Async requests are made in parallel, so each request is associated with an id to
    retrieve it from a list of responses.
    """

    id: str
    url: str
    params: dict


class AsyncResponseContext(BaseModel):
    """
    Structure used to return the response of an async request.
    Async requests are made in parallel, so each response is associated with the id it was
    used to make the request.
    """

    id: str
    response: dict


class Proxy(BaseModel):
    protocol: str = "https"
    url: str


def handle_clerk_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClerkAuthUnsupportedError as e:
            raise BigdataClientAuthFlowError(e)
        except ClerkUnexpectedSignInParametersError as e:
            raise BigdataClientAuthFlowError(e)
        except ClerkInvalidCredentialsError as e:
            raise BigdataClientAuthFlowError(e)
        except ClerkTooManySignInAttemptsError as e:
            raise BigdataClientTooManySignInAttemptsError(e)
        except ClerkAuthError as e:
            raise BigdataClientError(e)

    return wrapper


class Auth:
    """
    Class that performs the authentication logic, and wraps all the http calls
    so that it can handle the token autorefresh when needed.
    """

    def __init__(
        self,
        token_manager: ClerkTokenManager,
        pool_maxsize: int,
        verify: Union[bool, str],
        proxies: Optional[dict] = None,
    ):
        self._session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_maxsize=pool_maxsize)
        self._session.mount("https://", adapter)
        if proxies:
            self._session.proxies.update(proxies)
        self.verify = verify
        self._session.verify = verify
        self._token_manager = token_manager
        self._token_valid_event = threading.Event()
        self._token_valid_event.set()  # So the event doesn't block

    @classmethod
    @handle_clerk_exceptions
    def from_username_and_password(
        cls,
        username: str,
        password: str,
        clerk_frontend_url: str,
        clerk_instance_type: ClerkInstanceType,
        pool_maxsize: int,
        proxy: Optional[Proxy],
        verify: Union[bool, str],
    ) -> "Auth":

        proxies = {proxy.protocol: proxy.url} if proxy else None
        # A token manager handles the authentication flow and stores a jwt. It contains methods for refreshing it.
        token_manager = token_manager_factory(
            instance_type=clerk_instance_type,
            sign_in_strategy=SignInStrategyType.PASSWORD,
            clerk_frontend_url=clerk_frontend_url,
            email=username,
            password=password,
            pool_maxsize=pool_maxsize,
            proxies=proxies,
            verify=verify,
        )
        token_manager.refresh_session_token()
        return cls(
            token_manager=token_manager,
            pool_maxsize=pool_maxsize,
            proxies=proxies,
            verify=verify,
        )

    @handle_clerk_exceptions
    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        json=None,
        stream=None,
    ):
        """Makes an HTTP request, handling the token refresh if needed"""
        # Wait until token is valid - do not make requests if token was marked as invalid/expired.
        self._token_valid_event.wait(timeout=THREAD_WAIT_TIMEOUT)

        headers = headers or {}

        # 'https://api.bigdata.com/cqs/query-chunks' -> 'https://api.bigdata.com'
        parsed_url = urlparse(url)
        url_no_path = f"{parsed_url.scheme}://{parsed_url.netloc}"

        headers["origin"] = url_no_path
        headers["referer"] = url_no_path
        # if "content-type" not in headers:
        # We may have to conditionally set the content type when uploading files
        headers["content-type"] = "application/json"
        headers["accept"] = "application/json"
        headers["user-agent"] = get_user_agent(settings.PACKAGE_NAME)
        headers["Authorization"] = f"Bearer {self._token_manager.get_session_token()}"

        # The request method has other arguments but we are not using them currently
        response = self._session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            json=json,
            stream=stream,
        )
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            # Only the first failing call should try to refresh the token. If refreshing is already in progress [by another thread], then skip it.
            if self._token_valid_event.is_set():
                # Clear the event to indicate that token is invalid. Since now all calls to the requests will get blocked.
                self._token_valid_event.clear()
                # This headers.copy() is needed for testing. Mock lib does not make a copy, instead it points to
                # the original headers, so asserting that the headers changed fails.
                headers = headers.copy()
                headers["Authorization"] = (
                    f"Bearer {self._token_manager.refresh_session_token()}"
                )
                # Set the event to indicate that token is valid again. All the threads will now be able to execute the requests.
                self._token_valid_event.set()
            else:
                self._token_valid_event.wait(timeout=THREAD_WAIT_TIMEOUT)
                headers["Authorization"] = (
                    f"Bearer {self._token_manager.get_session_token()}"
                )

            # Retry the request
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                json=json,
                stream=stream,
            )

        return response

    @handle_clerk_exceptions
    def async_requests(
        self, method: str, request_contexts: list[AsyncRequestContext]
    ) -> list[AsyncResponseContext]:
        """Makes an async HTTP request, handling the token refresh if needed"""
        # 'https://api.bigdata.com/cqs/query-chunks' -> 'https://api.bigdata.com'
        if any(
            request_context.url != request_contexts[0].url
            for request_context in request_contexts
        ):
            raise ValueError(
                "All requests must have the same URL sice with the current logic origin/referer are "
                "shared across all requests."
            )
        parsed_url = urlparse(request_contexts[0].url)
        url_no_path = f"{parsed_url.scheme}://{parsed_url.netloc}"
        headers = {
            "origin": url_no_path,
            "referer": url_no_path,
            "content-type": "application/json",
            "accept": "application/json",
            "user-agent": get_user_agent(settings.PACKAGE_NAME),
            "Authorization": f"Bearer {self._token_manager.get_session_token()}",
        }

        try:
            return asyncio.run(
                self._create_and_resolve_tasks(method, headers, request_contexts)
            )
        # If any request raises HTTPStatus.UNAUTHORIZED refresh the token and use it again for all of the requests
        except aiohttp.client_exceptions.ClientResponseError as err:
            if err.status != HTTPStatus.UNAUTHORIZED:
                raise

            # This headers.copy() is needed for testing. Mock lib does not make a copy, instead it points to
            # the original headers, so asserting that the headers changed fails.
            headers = headers.copy()
            headers["Authorization"] = (
                f"Bearer {self._token_manager.refresh_session_token()}"
            )

            try:
                return asyncio.run(
                    self._create_and_resolve_tasks(method, headers, request_contexts)
                )
            except aiohttp.client_exceptions.ClientResponseError as err:
                if err.status == HTTPStatus.UNAUTHORIZED:
                    warnings.warn(DEPRECATED_WARNING_AUTOSUGGEST)
                raise

    async def _create_and_resolve_tasks(
        self, method: str, headers: dict, requests_contexts: list[AsyncRequestContext]
    ) -> list[AsyncResponseContext]:
        ssl_verification = self.verify
        if isinstance(self.verify, str):
            ssl_context = ssl.create_default_context()
            ssl_context.load_cert_chain(
                certfile=self.verify, keyfile=None, password=None
            )
            ssl_verification = ssl_context
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(
                    self._make_async_request(
                        method,
                        headers,
                        session,
                        request_context,
                        ssl_verification=ssl_verification,
                    )
                )
                for request_context in requests_contexts
            ]
            return await asyncio.gather(*tasks)

    async def _make_async_request(
        self,
        method: str,
        headers: dict,
        session: aiohttp.ClientSession,
        request_context: AsyncRequestContext,
        ssl_verification: Union[bool, ssl.SSLContext],
    ) -> AsyncResponseContext:

        target_scheme = urlparse(request_context.url).scheme

        proxy = (
            os.environ.get("ALL_PROXY")
            or os.environ.get(f"{target_scheme.upper()}_PROXY")
            or self._session.proxies.get(target_scheme)
        )

        async with session.request(
            method=method,
            headers=headers,
            params=request_context.params,
            url=request_context.url,
            raise_for_status=True,
            proxy=proxy,
            ssl=ssl_verification,
        ) as response:
            response = await response.json()

        return AsyncResponseContext(id=request_context.id, response=response)
