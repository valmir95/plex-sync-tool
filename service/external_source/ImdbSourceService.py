from service.external_source.SourceService import SourceService
from bs4 import BeautifulSoup
from model.external_source.media.ExternalSourceMedia import ExternalSourceMedia
import requests
from util.URLUtil import URLUtil


class ImdbSourceService(SourceService):
    def __init__(self, external_source, config, source_type):
        super().__init__(external_source, config, source_type)

    def get_media_items_from_external_playlist(self, external_url):
        source_type_val = self.get_external_source().get_source_type().value.lower()
        url_slash_split = external_url.split("/")
        is_valid_service = False
        for url_part in url_slash_split:
            if source_type_val in url_part:
                is_valid_service = True

            if is_valid_service:
                if url_part == "list":
                    return self.get_media_items_from_list(external_url)
                elif url_part == "chart":
                    return self.get_media_items_from_chart(external_url)
                elif url_part == "search":
                    return self.get_media_items_from_search(external_url)

        raise Exception("The url specified is not a valid IMDB link. Check the URL again.")

    def get_media_items_from_list(self, list_url):
        media_exists = True
        media_items = []
        page_counter = 1
        while media_exists:
            print("Scraping page " + str(page_counter) + " of list: " + str(list_url))
            media_exists = False
            # req_url = self.external_source.get_base_url() + "/list/" + str(external_id) + "/"
            req_url = list_url
            if page_counter > 1:
                req_url = req_url + "?page=" + str(page_counter)
            headers = {"Accept-Language": "en-US"}
            res = requests.get(req_url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            movie_elements = soup.find_all("div", class_="lister-item mode-detail")
            for movie_elem in movie_elements:
                title = movie_elem.h3.a.text
                imdb_id = movie_elem.div.attrs.get("data-tconst", None)
                source_media = ExternalSourceMedia()
                source_media.set_media_name(title)
                source_media.set_media_id(imdb_id)
                source_media.set_source_type(self.source_type)
                source_media.set_external_url(list_url)
                media_items.append(source_media)
                media_exists = True
            page_counter += 1
        print("Finished scraping")
        return media_items

    def get_media_items_from_chart(self, chart_url):
        media_items = []
        headers = {"Accept-Language": "en-US"}
        res = requests.get(chart_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        movie_elements = soup.find("tbody", class_="lister-list").find_all("tr")
        print("Scraping from chart: " + chart_url)
        for movie_elem in movie_elements:
            title = movie_elem.find("td", class_="titleColumn").a.text
            imdb_id = movie_elem.find("td", class_="watchlistColumn").div.attrs.get("data-tconst", None)
            source_media = ExternalSourceMedia()
            source_media.set_media_name(title)
            source_media.set_media_id(imdb_id)
            source_media.set_source_type(self.source_type)
            source_media.set_external_url(chart_url)
            media_items.append(source_media)
        return media_items

    def get_media_items_from_search(self, search_url):
        INCREMENT_SIZE = 50
        search_url_util = URLUtil(search_url)
        start_count = 1
        media_exists = True
        media_items = []
        while media_exists:
            media_exists = False
            req_url = search_url
            print("Scraping from item " + str(start_count) + " of list: " + str(search_url))
            if "start=" not in req_url:
                req_url += "&start=" + str(start_count)
            headers = {"Accept-Language": "en-US"}
            res = requests.get(req_url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            movie_elements = soup.find_all("div", class_="lister-item mode-advanced")
            for movie_elem in movie_elements:
                title = movie_elem.find("div", {"class": "lister-item-content"}).h3.a.text
                imdb_id = movie_elem.find("div", {"class": "lister-top-right"}).div.attrs.get("data-tconst", None)
                source_media = ExternalSourceMedia()
                source_media.set_media_name(title)
                source_media.set_media_id(imdb_id)
                source_media.set_source_type(self.source_type)
                source_media.set_external_url(search_url)
                media_items.append(source_media)
                media_exists = True
            start_count += INCREMENT_SIZE
        return media_items
        """
        search_query_params = search_url_util.get_query().split("?")[0].split("&")
        start_count = 0
        for param in search_query_params:
            if "start=" in param:
                start_count = int(param.split("=")[1])
        """

        raise Exception("Search url got called on but got dunked the fuck on")
