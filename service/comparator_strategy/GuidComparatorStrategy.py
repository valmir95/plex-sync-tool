from service.comparator_strategy.ComparatorStrategy import ComparatorStrategy
from model.plex.PlexGuid import PlexGuid
from model.plex.PlexMediaItem import PlexMediaItem


class GuidComparatorStrategy(ComparatorStrategy):
    def compare_external_and_plex_media(self, external_media, plex_media):
        for guid in plex_media.guids:
            try:
                plex_guid = PlexGuid.create_from_str(guid.id)

                if plex_guid.get_source_type() == external_media.get_source_type():
                    if plex_guid.get_guid_id() == external_media.get_media_id():
                        return PlexMediaItem(
                            plex_media,
                            external_media.get_external_url(),
                            external_media.get_media_id(),
                        )
            except Exception as e:
                print(str(e))

        return None