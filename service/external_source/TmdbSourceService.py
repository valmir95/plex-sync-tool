from service.external_source.SourceService import SourceService
from bs4 import BeautifulSoup
from model.external_source.media.ExternalSourceMedia import ExternalSourceMedia
import requests


class TmdbSourceService(SourceService):
    def __init__(self, external_source, config, source_type):
        self.comparator_strategy = None
        super().__init__(external_source, config, source_type, self.comparator_strategy)

    def get_media_items_from_external_playlist(self, external_url):
        raise Exception("TMDB not implemented")
