from abc import ABC, abstractmethod
from typing import List
from service.comparator_strategy.ComparatorStrategy import ComparatorStrategy


class SourceService(ABC):
    def __init__(self, external_source, config, source_type, comparator_strategy):
        self.external_source = external_source
        self.config = config
        self.source_type = source_type
        self.comparator_strategy = comparator_strategy

    @abstractmethod
    def get_media_from_external_playlist(self, external_url):
        pass

    @abstractmethod
    def get_allowed_comparator_strategies(self) -> List[ComparatorStrategy]:
        pass

    def get_external_source(self):
        return self.external_source

    def get_config(self):
        return self.config

    def get_source_type(self):
        return self.source_type

    def get_comparator_strategy(self):
        return self.comparator_strategy

    def set_external_source(self, external_source):
        self.external_source = external_source

    def set_config(self, config):
        self.config = config

    def set_source_type(self, source_type):
        self.source_type = source_type

    def set_comparator_strategy(self, comparator_strategy):
        self.comparator_strategy = comparator_strategy

    # TODO: See if we should put this somewhere else?
    def get_plex_media_items_from_external_id(self, plex_medias, external_url):
        items = []
        for plex_media in plex_medias:
            if plex_media.get_list_url() == external_url:
                items.append(plex_media)

        return items
