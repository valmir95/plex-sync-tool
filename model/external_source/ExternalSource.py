from abc import ABC, abstractmethod

# TODO: I don't think we need to have this as an abstract class any longer. We probably only need one class.
class ExternalSource(ABC):
    def __init__(self, base_url, source_type=None) -> None:
        self.base_url = base_url
        self.source_type = source_type

    def get_base_url(self):
        return self.base_url

    def get_source_type(self):
        return self.source_type

    def set_base_url(self, base_url):
        self.base_url = base_url

    def set_source_type(self, source_type):
        self.source_type = source_type

    @abstractmethod
    def get_id_from_guid(self, guid):
        pass

    @abstractmethod
    def get_id_from_url(self, url):
        pass