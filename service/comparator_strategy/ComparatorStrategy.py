from abc import ABC, abstractmethod


class ComparatorStrategy(ABC):
    @abstractmethod
    def compare_external_and_plex_media(self, external_media, plex_media):
        pass
