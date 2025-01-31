from dataclasses import dataclass
from typing import Iterable, Iterator, Optional, Union

from bigdata_client.advanced_search_query import AdvancedSearchQuery
from bigdata_client.api.search import (
    QueryChunksResponse,
    SavedSearchResponse,
    SaveSearchRequest,
    ShareSavedSearchRequest,
    UpdateSearchRequest,
    UserQueryShareCompanyContext,
)
from bigdata_client.connection import BigdataConnection
from bigdata_client.constants import MAX_SEARCH_PAGES
from bigdata_client.daterange import AbsoluteDateRange, RollingDateRange
from bigdata_client.document import Document
from bigdata_client.models.advanced_search_query import QueryComponent
from bigdata_client.models.comentions import Comentions
from bigdata_client.models.search import DocumentType, SortBy
from bigdata_client.models.sharing import SharePermission


class Search:
    """
    Class representing a search, saved or not.
    It allows you to perform searches in bigdata, getting documents, or get the
    co-mentions for that search.
    It also allows you to save, update, delete and share the search.
    """

    @dataclass
    class SearchUsage:
        """
        Internal class to hold the usage across a chain of Search objects.
        Whenever a Search is executed it creates a new Search object that actually performs the execution,
        this class is used to keep a mutable reference.
        FIXME: Remove when we get rid of the make_copy methods across the project.
        """

        usage: int

    def __init__(
        self,
        api: BigdataConnection,
        query: AdvancedSearchQuery,
        id: Optional[str] = None,
        name: str = "",
        company_shared_permission: Optional[SharePermission] = None,
        initial_usage: Optional[SearchUsage] = None,
    ):
        self._api: BigdataConnection = api
        self.id: Optional[str] = id
        self.name: str = name
        self.query: AdvancedSearchQuery = query
        self._company_shared_permission = company_shared_permission
        self._usage = initial_usage or Search.SearchUsage(0)

    @classmethod
    def from_query(
        cls,
        api: "BigdataConnection",
        query: QueryComponent,
        date_range: Optional[Union[AbsoluteDateRange, RollingDateRange]] = None,
        sortby: SortBy = SortBy.RELEVANCE,
        scope: DocumentType = DocumentType.ALL,
        rerank_threshold: Optional[float] = None,
    ) -> "Search":
        """
        Create a search object given a query, a date range, a scope filter and sort by
        """
        rpx_query = AdvancedSearchQuery(
            date_range=date_range,
            query=query,
            sortby=sortby,
            scope=scope,
            rerank_threshold=rerank_threshold,
        )
        return cls(api=api, query=rpx_query)

    @classmethod
    def from_saved_search_response(
        cls, api: BigdataConnection, response: SavedSearchResponse
    ):
        # Internal method to parse an API response. Do not document
        simple_query = AdvancedSearchQuery.from_saved_search_response(response.query)
        company_permission = response.shared.company.permission
        if company_permission == SharePermission.UNDEFINED:
            company_permission = None

        return cls(
            api=api,
            query=simple_query,
            id=response.id,
            name=response.name,
            company_shared_permission=company_permission,
            # TODO: Add the rest of the parameters like created_at, updated_at,
            # owner, etc.
        )

    def limit_documents(self, limit: int) -> Iterable[Document]:
        """Return the first `limit` documents of the search as a generator"""
        new = self.make_copy()
        return SearchResults(new, limit=limit)

    def run(self, limit: int) -> list[Document]:
        """Return the first `limit` documents of the search as a list"""
        return list(self.limit_documents(limit))

    def get_comentions(self) -> Comentions:
        """Get the comentions of the search"""
        if self._api is None:
            raise ValueError("The search object must have an API to get comentions.")
        request = self.query.to_discovery_panel_api_request()
        response = self._api.query_discovery_panel(request)
        return Comentions.from_response(response)

    def make_copy(self):
        query = self.query.make_copy()
        return Search(
            self._api,
            id=self.id,
            name=self.name,
            query=query,
            company_shared_permission=self._company_shared_permission,
            initial_usage=self._usage,
        )

    def get_usage(self) -> int:
        """Get the usage of the search"""
        return int(self._usage.usage / 10)

    def _get_query_chunks_page(self, page: int = 1) -> QueryChunksResponse:
        if self._api is None:
            raise ValueError("The search object must have an API to get pages.")
        request = self.query.to_query_chunks_api_request(page)
        query_chunks_response = self._api.query_chunks(request)
        self._usage.usage += query_chunks_response.chunks_count
        return query_chunks_response

    def save(self, name: str):
        """
        Saves a search.

        After it has been saved, the ``id`` property of the search object will be set.
        """
        if self._api is None:
            raise ValueError("The search object must have an API to save.")
        if self.id is None:
            # Create a new search
            request = SaveSearchRequest(
                name=name, query=self.query.to_save_search_request()
            )
            response = self._api.save_search(request)
            self.id = response.id
        else:
            # Update an existing search
            request = UpdateSearchRequest(
                name=name, query=self.query.to_save_search_request()
            )
            self._api.update_search(request, self.id)

    def delete(self):
        """Deletes a saved search"""
        if self._api is None:
            raise ValueError("The search object must have an API to delete.")
        if self.id is None:
            raise ValueError("The search object is not saved.")
        self._api.delete_search(self.id)
        self.id = None

    @property
    def is_saved(self) -> bool:
        """Returns whether this search is saved or not. Read-only."""
        return self.id is not None

    def share_with_company(self):
        """
        Shares a search with the whole company.

        Note: If the search query contains one or more private watchlists,
        those will get automatically shared as well.
        """
        if self._api is None:
            raise ValueError("The search object must have an API to share.")
        if self.id is None:
            raise ValueError("The search object is not saved.")
        request = ShareSavedSearchRequest(
            company=UserQueryShareCompanyContext(permission=SharePermission.READ),
            users=[],
        )
        self._api.share_search(self.id, request)
        self._company_shared_permission = SharePermission.READ

    def unshare_with_company(self):
        """Makes a shared search (that you own) private"""
        if self._api is None:
            raise ValueError("The search object must have an API to unshare.")
        if self.id is None:
            raise ValueError("The search object is not saved.")
        request = ShareSavedSearchRequest(
            company=UserQueryShareCompanyContext(permission=SharePermission.UNDEFINED),
            users=[],
        )
        self._api.share_search(self.id, request)
        self._company_shared_permission = None

    @property
    def company_shared_permission(self) -> Optional[SharePermission]:
        """
        The permission of this search on the company.

        Note that this can't be changed directly, and is ignored on the ``save()`` method. To
        change it, use the ``share_with_company()`` and ``unshare_with_company()`` methods.
        """
        return self._company_shared_permission


# To be changed. It shouldn't be a dataclass, but for now it's fine
@dataclass
class SearchResults:
    """
    A search with a limit. It allows you to get the count of documents, and/or get
    an iterator over the results.
    """

    def __init__(self, search: Search, limit: int):
        self.search = search
        self._first_page: Optional[QueryChunksResponse] = None
        if limit <= 0:
            raise ValueError("The limit must be a positive number.")
        self._limit_documents = limit

    @property
    def _sentence_count(self) -> int:
        """
        INTERNAL!!
        Do not rely on this because it may not mean what you think it means, and
        could change.
        """
        first_page = self._ensure_first_page()
        return first_page.count

    @property
    def _document_count(self) -> int:
        """
        INTERNAL!!
        Do not rely on this because it may not mean what you think it means.
        """
        first_page = self._ensure_first_page()
        return first_page.document_count

    def _ensure_first_page(self) -> QueryChunksResponse:
        if self._first_page is None:
            self._first_page = self.search._get_query_chunks_page()
        return self._first_page

    def __iter__(self) -> Iterable[Document]:
        return iter(
            SearchResultsPaginatorIterator(
                self.search, self._limit_documents, self._first_page
            )
        )


class SearchResultsPaginatorIterator:
    """
    Helper to iterate over the documents in all the pages.
    Optionally, it can skip the first request and use the first_page parameter.
    """

    def __init__(
        self,
        search: Search,
        limit: int,
        first_page: Optional[QueryChunksResponse],
    ):
        self.search = search
        self.current_page = first_page or None
        self._limit = limit
        self._page_num = 0

    def __iter__(self) -> Iterator[Document]:
        # The first page may have been provided, if the user asked for the count first
        if self.current_page is None:
            self.current_page = self.search._get_query_chunks_page()
        items = 0
        for _ in range(MAX_SEARCH_PAGES):  # Effectively a while(True), but safer
            for document in self.current_page.stories:
                if items >= self._limit:
                    return
                items += 1
                yield Document.from_response(document, api=self.search._api)
            next_page = (
                self.current_page.next_cursor  # Double-check, if there are no elements, don't trust next_cursor
                if self.current_page.stories
                else None
            )
            if not next_page:
                break
            self._page_num = next_page
            self.current_page = self.search._get_query_chunks_page(self._page_num)
