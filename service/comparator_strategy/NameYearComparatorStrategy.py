from service.comparator_strategy.ComparatorStrategy import ComparatorStrategy
from model.plex.PlexMediaItem import PlexMediaItem


class NameYearComparatorStrategy(ComparatorStrategy):
    def compare_external_and_plex_media(self, external_media, plex_media):
        if self.get_clean_title(plex_media.title) == external_media.get_media_name():
            if external_media.get_year():
                if plex_media.year == external_media.get_year().year:
                    return PlexMediaItem(plex_media, external_media.get_external_url(), external_media.get_media_id())
        return None

    def get_clean_title(self, title):
        return title.split("(")[0].rstrip()