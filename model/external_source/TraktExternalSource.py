from model.external_source.ExternalSource import ExternalSource
from model.external_source.enum.ExternalSourceType import ExternalSourceType
from model.external_source.enum.ExternalSourceUrl import ExternalSourceUrl


class TraktExternalSource(ExternalSource):
    def __init__(self) -> None:
        self.base_url = ExternalSourceUrl.TRAKT
        self.source_type = ExternalSourceType.TRAKT
        super().__init__(self.base_url, self.source_type)

    def get_id_from_guid(self, guid):
        raise Exception("Method not implemented")

    def get_id_from_url(self, url):
        raise Exception("Method not implemented")