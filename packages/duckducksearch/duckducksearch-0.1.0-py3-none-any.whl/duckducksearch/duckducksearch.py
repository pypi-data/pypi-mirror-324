import logging
from time import time, sleep
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


class DuckDuckSearchError(Exception):
    """
    Exception for errors in the DuckDuckSearch component.
    """
    pass


@dataclass
class Document:
    """
    A simple data class to store document information.
    """
    title: str
    content: str
    link: str


class DuckDuckSearch:
    """
    Uses DuckDuckGo to search for relevant documents on the internet.

    Example usage:
    ```python
    from duckduck_search_lib.duckduck_search import DuckDuckSearch

    searcher = DuckDuckSearch(top_k=10, max_results=20)
    results = searcher.search("What is Python?", 5)
    print(results)
    ```
    """

    def __init__(
        self,
        top_k: Optional[int] = 10,
        max_results: Optional[int] = 10,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        backend: str = "api",
        allowed_domain: str = "",
        timeout: int = 10,
        use_answers: bool = False,
        proxy: Optional[str] = None,
        max_search_frequency: float = float('inf')
    ):
        """
        Initialize the DuckDuckSearch component.
        """
        self.top_k = top_k
        self.max_results = max_results
        self.region = region
        self.safesearch = safesearch
        self.timelimit = timelimit
        self.backend = backend
        self.allowed_domain = allowed_domain
        self.timeout = timeout
        self.use_answers = use_answers

        self.proxy = proxy
        self.ddgs = DDGS(proxy=self.proxy)

        self.max_search_frequency = max_search_frequency
        self.last_search_time = 0

    def _rate_limit(self):
        """
        Applies rate limiting to search requests based on max_search_frequency.
        """
        if self.max_search_frequency != float('inf'):
            current_time = time()
            time_since_last_search = current_time - self.last_search_time
            time_to_wait = max(0.0, self.max_search_frequency - time_since_last_search)
            if time_to_wait > 0:
                sleep(time_to_wait)
            self.last_search_time = time()

    def search(self, query: str, num_results: int) -> Dict[str, Union[List[Document], List[str]]]:
        """
        Perform a search using DuckDuckGo.

        :param query: The search query string.
        :param num_results: The number of results to return.
        :returns: A dictionary with keys:
                    - "documents": list of Document objects,
                    - "links": list of URLs.
        :raises ValueError: If the query parameter is empty.
        :raises DuckDuckSearchError: If an error occurs during the search.
        """
        if not query:
            raise ValueError("The 'query' parameter cannot be empty.")

        self._rate_limit()
        effective_count = num_results

        documents: List[Document] = []

        if self.use_answers:
            try:
                answers = self.ddgs.answers(query)
            except Exception as e:
                raise DuckDuckSearchError(f"An error occurred during the search: {e}") from e
            for answer in answers:
                documents.append(
                    Document(
                        title="",
                        content=answer.get("text", ""),
                        link=answer.get("url", "")
                    )
                )

        query_formatted = f"site:{self.allowed_domain} {query}" if self.allowed_domain else query
        payload = {
            "keywords": query_formatted,
            "max_results": effective_count,
            "region": self.region,
            "safesearch": self.safesearch,
            "timelimit": self.timelimit,
            "backend": self.backend
        }

        try:
            results = self.ddgs.text(**payload)
        except Exception as e:
            raise DuckDuckSearchError(f"An error occurred during the search: {e}") from e

        for result in results:
            documents.append(
                Document(
                    title=result.get("title", ""),
                    content=result.get("body", ""),
                    link=result.get("href", "")
                )
            )

        links = [result.get("href", "") for result in results]

        logger.debug("DuckDuckGo returned %d documents for the query '%s'",
                     len(documents), query)

        return {
            "documents": documents[:effective_count],
            "links": links[:effective_count]
        }
