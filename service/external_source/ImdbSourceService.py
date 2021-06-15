from service.external_source.SourceService import SourceService
from bs4 import BeautifulSoup
from model.external_source.media.ExternalSourceMedia import ExternalSourceMedia
import requests
from util.URLUtil import URLUtil
from service.comparator_strategy.GuidComparatorStrategy import GuidComparatorStrategy
from service.comparator_strategy.ComparatorStrategy import ComparatorStrategy
from model.shared.enum.TVRating import TVRating
from model.shared.enum.MovieRating import MovieRating
from model.shared.enum.MediaType import MediaType
from typing import List


class ImdbSourceService(SourceService):
    def __init__(self, external_source, config, source_type):
        self.comparator_strategy = GuidComparatorStrategy()
        super().__init__(external_source, config, source_type, self.comparator_strategy)

    def get_allowed_comparator_strategies(self) -> List[ComparatorStrategy]:
        return [GuidComparatorStrategy()]

    def get_media_from_external_playlist(self, external_url):
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
            req_url = list_url
            if page_counter > 1:
                req_url = req_url + "?page=" + str(page_counter)
            headers = {"Accept-Language": "en-US"}
            res = requests.get(req_url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            media_elements = soup.find_all("div", class_="lister-item mode-detail")
            for media_elem in media_elements:
                title = media_elem.h3.a.text
                imdb_id = media_elem.div.attrs.get("data-tconst", None)
                media_type = self.get_media_type_from_media_element(media_elem)
                year_elem = (
                    media_elem.find("span", class_="lister-item-year").text.strip().replace("(", "").replace(")", "")
                )
                source_media = ExternalSourceMedia()
                source_media.set_media_name(title)
                source_media.set_media_id(imdb_id)
                source_media.set_source_type(self.source_type)
                source_media.set_external_url(list_url)
                source_media.set_media_type(media_type)
                media_items.append(source_media)
                media_exists = True
            page_counter += 1
        print("Finished scraping")
        return media_items

    def get_media_items_from_chart(self, chart_url):
        # This is the ONLY identifier on an IMDB chart page that determines if a title is a TV-SHOW
        TV_LINK_MEDIA_TYPE_IDENTIFIER = "chttvm"
        media_items = []
        headers = {
            "Accept-Language": "en-US",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }
        res = requests.get(chart_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        media_elements = soup.find("tbody", class_="lister-list").find_all("tr")
        print("Scraping from chart: " + chart_url)
        for media_elem in media_elements:
            title = media_elem.find("td", class_="titleColumn").a.text
            imdb_id = media_elem.find("td", class_="watchlistColumn").div.attrs.get("data-tconst", None)
            title_link = media_elem.find("td", class_="titleColumn").a["href"]
            media_type = MediaType.MOVIE
            if TV_LINK_MEDIA_TYPE_IDENTIFIER in title_link:
                media_type = MediaType.TV
            source_media = ExternalSourceMedia()
            source_media.set_media_name(title)
            source_media.set_media_id(imdb_id)
            source_media.set_source_type(self.source_type)
            source_media.set_external_url(chart_url)
            source_media.set_media_type(media_type)
            media_items.append(source_media)
        return media_items

    def get_media_items_from_search(self, search_url):
        INCREMENT_SIZE = 50
        RESULT_LIMIT = 1500
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
            media_elements = soup.find_all("div", class_="lister-item mode-advanced")
            for media_elem in media_elements:
                title = media_elem.find("div", {"class": "lister-item-content"}).h3.a.text
                imdb_id = media_elem.find("div", {"class": "lister-top-right"}).div.attrs.get("data-tconst", None)
                media_type = self.get_media_type_from_media_element(media_elem)
                source_media = ExternalSourceMedia()
                source_media.set_media_name(title)
                source_media.set_media_id(imdb_id)
                source_media.set_source_type(self.source_type)
                source_media.set_external_url(search_url)
                source_media.set_media_type(media_type)
                media_items.append(source_media)
                media_exists = True
            if start_count > RESULT_LIMIT:
                break
            start_count += INCREMENT_SIZE
        return media_items

    def get_media_type_from_media_element(self, media_element):
        media_type = MediaType.MOVIE
        certificate_rating = media_element.find("span", class_="certificate")
        if certificate_rating:
            certificate_rating = certificate_rating.text.upper()
            tv_rating = TVRating.from_str(certificate_rating)
            if tv_rating:
                media_type = MediaType.TV

        return media_type