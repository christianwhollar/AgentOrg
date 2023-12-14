from tools.search_engines.google_search import GoogleSearch
from tools.web_utils.web_search import SearchEngine, WebSearch
import re
from tools.tool import Tool

class SearchTool(Tool):
    def __init__(self):
        self.engine = SearchEngine(GoogleSearch)
        self.state = 'Ready'
        self.links = {}

    @property
    def identifier(self) -> str:
        return 'Search Mode'

    @property
    def command(self) -> str:
        return ' To perform an internet search, say SEARCH.'
    
    @property
    def example(self) -> str:
        return ' User says: I want to learn more about Python. Agent says: SEARCH. You are the agent.'

    def run(self, response):

        if self.state == 'Ready' and 'SEARCH' in response:
            self.state = 'Search'
            return 'Give me exactly what to put in the search engine.'
        
        elif self.state == 'Search':
            self.web_search = WebSearch(self.engine, query=response)
            links = self.web_search.search()

            self.links = links
            self.state = 'Response Links'

            formatted_links = ', '.join([f'{index} {link}' for index, link in enumerate(links)])

            return f'Here are the links to your search result: {formatted_links}. Say the index number of the link you would like to open.'

        elif self.state == 'Response Links':
            match = re.search(r'\d', response)
            index_link = int(match.group()) if match else 0
            link = self.links[index_link]
            web_page = self.web_search.open(link)
            body = str(web_page.body)
            self.webpagebody = web_page.body
            self.state = 'Exit'            
            return f'Here is the result of your search: {body[:3000]}. You are now exiting SEARCH.'
        
        else:
            self.state = 'Ready'
            return None
