from tools.web_utils.exceptions import HTTPRequestError
from tools.search_engines.search_engine_base import SearchEngineBase
from tools.web_utils.web_link import WebLink
from typing import List
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class GoogleSearch(SearchEngineBase):
    def search(self) -> List[WebLink]:
        link = f"https://www.google.com/search?q={self._query}&start={self._current_page_number * 10}"
        logger.info(f'Searching Google with URL: {link}')
        response = requests.get(link)
        # Checking for a successful response
        if response.status_code != 200:
            raise HTTPRequestError(f'Failed to retrieve {link}: {response.status_code}')
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [WebLink(self.extract_url(a['href'])) for a in soup.find_all('a', href=True) if 'url?q=' in a['href'] and 'webcache' not in a['href']]
        return links