from model.external_source.ExternalSource import ExternalSource


class TmdbSource(ExternalSource):
    def __init__(self, base_url, api_source=None) -> None:
        self.base_url = base_url
        self.api_source = api_source

    def get_id_from_guid(self, guid):
        raise Exception("Method not implemented")

    def get_id_from_url(self, url):
        raise Exception("Method not implemented")