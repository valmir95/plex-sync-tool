from typing import SupportsRound


class ExternalSource(object):
    def __init__(self, base_url, api_source=None, source_type=None) -> None:
        self.base_url = base_url
        self.api_source = api_source
        self.source_type = source_type

    def get_base_url(self):
        return self.base_url

    def get_api_source(self):
        return self.api_source

    def get_source_type(self):
        return self.source_type

    def set_base_url(self, base_url):
        self.base_url = base_url

    def set_api_source(self, api_source):
        self.api_source = api_source

    def set_source_type(self, source_type):
        self.source_type = source_type

    def get_id_from_guid(self, guid):
        raise Exception("Method not implemented")

    def get_id_from_url(self, url):
        raise Exception("Method not implemented")