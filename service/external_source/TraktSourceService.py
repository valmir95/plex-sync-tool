from service.external_source.SourceService import SourceService
from bs4 import BeautifulSoup
from model.external_source.media.ExternalSourceMedia import ExternalSourceMedia
import requests
from util.URLUtil import URLUtil


class TraktSourceService(SourceService):
    def __init__(self, external_source, config, source_type):
        super().__init__(external_source, config, source_type)

    def get_media_items_from_external_playlist(self, external_url):
        media_elements = []
        headers = {"Accept-Language": "en-US"}
        res = requests.get(external_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        movie_elements = soup.find_all("div", class_="grid-item col-xs-6 col-md-2 col-sm-3")
        for movie_elem in movie_elements:
            title = movie_elem.find("meta", {"itemprop": "name"}).attrs.get("content", None)
            title_parts = title.split(" ")
            title = ""
            year = None
            for title_part in title_parts:
                if title_part.startswith("(") and title_part.endswith(")"):
                    if title_part[1:5].isnumeric():
                        year = int(title_part[1:5])
                        break
                title += title_part + " "
            title = title.rstrip()
            movie_id = movie_elem.attrs.get("data-movie-id", None)
            source_media = ExternalSourceMedia(title, movie_id, self.source_type, external_url, year)
            media_elements.append(source_media)

        return media_elements

        # raise Exception("The url specified is not a valid IMDB link. Check the URL again.")
