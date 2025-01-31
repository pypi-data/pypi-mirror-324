class BigdataClientError(Exception):
    """
    Base exception for all BigdataClient exceptions.

    Contact support if this exception is raised.
    """

    pass


class RequestMaxLimitExceeds(BigdataClientError):
    """
    Request body size limit is set to 64KB (65536 bytes)
    In cases when request body size exceeds 64KB this exception will be thrown.

    Any method that sends requests can throw this exception.

    **Solution**: Please identify the method that caused the error and craft a smaller request.

    * **Search methods**: You could create several smaller and more concrete queries.
    * **Knowledge Graph methods or Watchlist methods**: You could split the list of parameters and call the same method multiple times.
    """

    def __init__(self, request_size: int, limit: int):
        super().__init__(f"Request body exceeds limit. Max Limit: {limit} bytes")
        self.request_size = request_size

    def __str__(self):
        return f"{self.args[0]} (Request Size: {self.request_size} bytes)"


class BigdataClientRateLimitError(BigdataClientError):
    """
    Too many requests in a short period of time. These are the current Bigdata.com platform rate limits:

    * 500 requests per minute per JWT session (We advise customers to instantiate a single Bigdata object per user).
    * 1500 requests per minute per IP.
    * Too many simultaneous uploads per user (By default 10 and customizable per organization).

    **Solution**: Adapt your code to make fewer requests.
    """


class BigdataClientAuthFlowError(BigdataClientError):
    """
    Generic error for authentication flow when the problem is not related to the rate limit.
    Possible causes:

    * Invalid credentials.
    * Invalid sign-in configuration.
    * Other authentication issues.

    **Solution**: Check the error message for more information. Contact support if necessary.
    """


class BigdataClientTooManySignInAttemptsError(BigdataClientError):
    """
    Too many sign-in attempts in a short period of time from the same IP address.

    * 7 requests per 10 seconds is a theoretical limit.

    **Solution**: Reuse the Bigdata instance across your project instead of creating it many times. In the case of
    distributed systems, consider a backoff strategy for retries.
    """


class BigdataClientIncompatibleStateError(BigdataClientError):
    """
    The current state of the object doesn't allow the operation to be executed.

    **Solution**:
        If raised when deleting a file: It means that the file can't be deleted until it finishes processing.
    """
