from warnings import showwarning
from service.external_source.SourceService import SourceService
from bs4 import BeautifulSoup
from model.external_source.media.ExternalSourceMedia import ExternalSourceMedia
import requests
from util.URLUtil import URLUtil
from model.shared.enum.MediaType import MediaType
from datetime import date, datetime


class TraktSourceService(SourceService):
    def __init__(self, external_source, config, source_type):
        super().__init__(external_source, config, source_type)

    def get_media_items_from_external_playlist(self, external_url):
        external_medias = []
        headers = {"Accept-Language": "en-US"}
        res = requests.get(external_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        media_elements = soup.find_all("div", class_="grid-item col-xs-6 col-md-2 col-sm-3")
        media_ids_added = []
        for media_element in media_elements:
            # TODO: Determine if we will continue to use year or switch entirely over to datetime objects.
            year = None
            year_elem = media_element.attrs.get("data-released", None)
            year = self.media_element_date_string_to_datetime(year_elem)
            media_type_str = media_element.attrs.get("data-type", None)
            if media_type_str == "movie":
                title = self.get_title_movie(media_element)
                media_type = MediaType.MOVIE
                media_id = media_element.attrs.get("data-movie-id", None)
            else:
                media_type = MediaType.TV
                is_part_of_show = media_type_str == "season" or media_type_str == "episode"
                title = self.get_title_show(media_element, is_part_of_show)
                media_id = media_element.attrs.get("data-show-id", None)

            if media_id not in media_ids_added:
                if media_type_str == "season" or media_type_str == "episode":
                    raw_date_str = self.fetch_release_date_for_show_part(media_id)
                    year = self.media_element_date_string_to_datetime(raw_date_str)
                source_media = ExternalSourceMedia()
                source_media.set_media_name(title)
                source_media.set_media_id(media_id)
                source_media.set_source_type(self.source_type)
                source_media.set_external_url(external_url)
                source_media.set_year(year)
                source_media.set_media_type(media_type)
                media_ids_added.append(media_id)
                external_medias.append(source_media)

        return external_medias

    def get_title_movie(self, media_element):
        title = media_element.find("meta", {"itemprop": "name"}).attrs.get("content", None)
        title_parts = title.split(" ")
        title = ""
        for title_part in title_parts:
            if title_part.startswith("(") and title_part.endswith(")"):
                if title_part[1:5].isnumeric():
                    break
            title += title_part + " "
        return title.rstrip()

    def get_title_show(self, media_element, is_part_of_show):
        if not is_part_of_show:
            return media_element.find("meta", {"itemprop": "name"}).attrs.get("content", None)
        return (
            media_element.find("span", {"itemprop": "partOfSeries"})
            .find("meta", {"itemprop": "name"})
            .attrs.get("content", None)
        )

    def fetch_release_date_for_show_part(self, media_id):
        show_url = "https://trakt.tv/shows/" + media_id
        headers = {"Accept-Language": "en-US"}
        res = requests.get(show_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        date_elem = soup.find("span", {"class": "convert-date"})
        if date_elem:
            return date_elem.text
        return None

    def media_element_date_string_to_datetime(self, date_string):
        media_date = None

        if date_string and date_string != "0":
            if "T" in date_string:
                media_date_raw = date_string.split("T")[0]
                media_date = datetime.strptime(media_date_raw, "%Y-%m-%d")
            else:
                media_date = datetime.strptime(date_string, "%Y-%m-%d")

        return media_date