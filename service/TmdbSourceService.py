from service.SourceService import SourceService
from bs4 import BeautifulSoup
from model.external_source.media.ExternalSourceMedia import ExternalSourceMedia
import requests


class TmdbSourceService(SourceService):
    def __init__(self, external_source, config):
        super().__init__(external_source, config)

    def get_media_items_from_external_playlist(self, external_id):
        raise Exception("Not implemented")
