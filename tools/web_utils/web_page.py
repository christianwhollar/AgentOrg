from rich.text import Text

class WebPageTitle:
    def __init__(self, title: str):
        self.title = title

    def __str__(self):
        return self.title

    def __rich__(self):
        return f"[bold underline green]{self.title}"
        
class WebPageBody:
    def __init__(self, body: str):
        self.body = body

    def __str__(self):
        return self.body

    def __rich__(self):
        return f"[italic green]{self.body}"
            
class WebPage:
    def __init__(self, soup:str = ''):
        self.soup = soup

    @property
    def title(self) -> WebPageTitle:
        if self.soup is None:
            raise Exception('WebLink has not been opened yet')
        title_tag = self.soup.find('title')
        return WebPageTitle(title_tag.text) if title_tag else None

    @property
    def body(self) -> WebPageBody:
        if self.soup is None:
            raise Exception('WebLink has not been opened yet')
        body_tag = self.soup.find('body')
        return WebPageBody(body_tag.text) if body_tag else None
