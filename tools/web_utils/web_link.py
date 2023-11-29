from rich.text import Text

class WebLink:
    def __init__(self, link: str):
        self.link = link

    def __str__(self):
        return str(Text(self.link, style="blue"))
