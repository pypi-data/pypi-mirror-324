from html.parser import HTMLParser

class LinkExtractor(HTMLParser):
    """Simple HTML parser to extract the URL link from the client redirection
    response."""
    link: str | None
    def handle_starttag(self, tag: str, attr: list[str]): ...
