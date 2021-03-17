from service.SourceService import SourceService
from bs4 import BeautifulSoup
from model.external_source.media.ExternalSourceMedia import ExternalSourceMedia
import requests


class ImdbSourceService(SourceService):
    def __init__(self, external_source, config, source_type):
        super().__init__(external_source, config, source_type)

    def get_media_items_from_external_playlist(self, external_id):
        media_exists = True
        media_items = []
        page_counter = 1
        while media_exists:
            print("Scraping page " + str(page_counter) + " of list: " + str(external_id))
            media_exists = False
            req_url = self.external_source.get_base_url() + "/list/" + str(external_id) + "/"
            if page_counter > 1:
                req_url = req_url + "?page=" + str(page_counter)
            headers = {"Accept-Language": "en-US"}
            res = requests.get(req_url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            movie_elements = soup.find_all("div", class_="lister-item mode-detail")
            for movie_elem in movie_elements:
                title = movie_elem.h3.a.text
                imdb_id = movie_elem.div.attrs.get("data-tconst", None)
                source_media = ExternalSourceMedia(title, imdb_id, self.source_type, external_id)
                media_items.append(source_media)
                media_exists = True
            page_counter += 1
        print("Finished scraping")
        return media_items
