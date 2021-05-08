from urllib.parse import urlparse


class URLUtil(object):
    def __init__(self, url):
        self.url = url
        self.parser = urlparse(url)

    def validate_url(self):
        return (self.parser.scheme == "https" or self.parser.scheme == "http") and self.parser.netloc.startswith("www")

    def get_netloc(self):
        return self.parser.netloc

    def get_path(self):
        return self.parser.path

    def get_query(self):
        return self.parser.query
