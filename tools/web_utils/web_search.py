# Standard Library Imports
import logging
from typing import List, Type

# Third-Party Library Imports
import requests
from bs4 import BeautifulSoup
import httpx  # If you're using it in this module

# Local Imports
from tools.search_engines.search_engine_base import SearchEngineBase
from tools.web_utils.web_link import WebLink
from tools.web_utils.web_page import WebPage
from tools.web_utils.exceptions import FetchException
from tools.decorators import log_method_call, retry_on_exception

logger = logging.getLogger(__name__)

class SearchEngine:
    def __init__(self, engine_class: Type[SearchEngineBase]):
        self.engine_class = engine_class

    def create_engine(self, query: str) -> SearchEngineBase:
        return self.engine_class(query)

class WebSearch:
    def __init__(self, engine: SearchEngine, query: str):
        self.engine = engine
        self.search_engine = self.engine.create_engine(query)

    def search(self, query: str = None) -> List[WebLink]:
        if query:
            self.search_engine._query = query  # Update query if provided
        return self.search_engine.search()

    def next_page(self) -> List[WebLink]:
        return self.search_engine.next_page()

    def prev_page(self) -> List[WebLink]:
        return self.search_engine.prev_page()

    @log_method_call  # Log method calls
    def print_links(self, links: List[WebLink]):
        for link in links:
            print(link)
    
    @retry_on_exception(max_retries=3, exceptions=(Exception,))  # Retry on exceptions
    def _open_sync(self, link: WebLink) -> WebPage:
        logger.info(f'Opening WebLink: {link.link}')
        try:
            response = requests.get(link.link)
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx and 5xx)
        except requests.RequestException as e:
            logger.error(f'Failed to retrieve {link}: {e}')
            raise FetchException(f'Failed to retrieve {link}: {e}')

        logger.info(f'Successfully retrieved {link}')
        soup = BeautifulSoup(response.text, 'html.parser')
        return WebPage(soup=soup)

    async def _open_async(self, link: WebLink) -> WebPage:
        async with httpx.AsyncClient() as client:
            response = await client.get(link.link)
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        return WebPage(soup=soup)

    def open(self, link: WebLink):
        # Determine whether to call the synchronous or asynchronous version
        if isinstance(link, WebLink):
            return self._open_sync(link)
        elif hasattr(link, '__await__'):
            return self._open_async(link)
        else:
            raise TypeError("Unsupported type for 'link' argument")