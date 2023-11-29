from abc import ABC, abstractmethod
from typing import List
from tools.web_utils.web_link import WebLink
from tools.web_utils.exceptions import InvalidPageIndexException
from urllib.parse import unquote

class SearchEngineBase(ABC):
    def __init__(self, query: str):
        self._query = query
        self._current_page_number = 0

    @abstractmethod
    def search(self) -> List[WebLink]:
        pass

    def next_page(self) -> List[WebLink]:
        self._current_page_number += 1
        return self.search()

    def prev_page(self) -> List[WebLink]:
        if self._current_page_number > 0:
            self._current_page_number -= 1
            return self.search()
        else:
            raise InvalidPageIndexException(f'{self._current_page_number} is not a valid page number.')

    @staticmethod
    def extract_url(url: str) -> str:
        partial_url = url.split('url?q=')[1] if 'url?q=' in url else url
        actual_url = partial_url.split('&')[0]
        actual_url = unquote(actual_url)
        return actual_url