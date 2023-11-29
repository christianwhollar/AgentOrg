class InvalidPageIndexException(Exception):
    def __init__(self, message:str ="The page index is invalid"):
        super().__init__(message)

class SearchEngineError(Exception):
    def __init__(self, message: str ="An error occurred in the search engine"):
        super().__init__(message)

class HTTPRequestError(SearchEngineError):
    def __init__(self, message:str ="HTTP request error", status_code=None):
        super().__init__(message)
        self.status_code = status_code

class ParsingError(SearchEngineError):
    def __init__(self, message: str ="Parsing error", parsing_context=None):
        super().__init__(message)
        self.parsing_context = parsing_context

class FetchException(Exception):
    def __init__(self, message: str ="Failed to fetch the webpage"):
        super().__init__(message)
        
class HTTPRequestError(SearchEngineError):
    def __init__(self, message: str = ''):
        super().__init__(message)
