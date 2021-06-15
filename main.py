from util.URLUtil import URLUtil
from service.config.ConfigParser import ConfigParser
from model.external_source.enum.ExternalSourceType import ExternalSourceType
from service.external_source.SourceServiceFactory import SourceServiceFactory
from service.plex.PlexAPIService import PlexAPIService
from service.thread_executor.PlexAPIServiceThreadExecutor import PlexAPIServiceThreadExecutor
import time
from service.thread_executor.ThreadBatchExecutor import ThreadBatchExecutor
from model.plex.PlexGuid import PlexGuid
from model.plex.PlexMediaItem import PlexMediaItem

# TODO: Replace Playlists with Collections, or have it as an advanced option in the config file.
# TODO: Split into more methods
# TODO: Create classes and class methods for some of the functionality in main.py
try:
    config_parser = ConfigParser("config.toml")
    config = config_parser.parse_config_file()
    plex_service = PlexAPIService(config.get_plex_base_url(), config.get_plex_api_token())
    cached_items = []
    start_time = time.time()
    for playlist_item in config.get_playlist_items():
        print("Starting sync of plex playlist: " + playlist_item.get_playlist_name())
        plex_medias = []
        for playlist_url in playlist_item.get_external_list_urls():
            source_service_factory = SourceServiceFactory(config)
            source_service = source_service_factory.get_source_service_from_url(playlist_url)
            temp_cached = source_service.get_plex_media_items_from_external_id(cached_items, playlist_url)
            if len(temp_cached) > 0:
                plex_medias.extend(temp_cached)
                print("List url: " + str(playlist_url) + " is already cached, so adding directly...")
            else:
                scraped_medias = source_service.get_media_from_external_playlist(playlist_url)
                plex_service_function = plex_service.get_plex_media_objs_from_external_media_objs.__name__
                thread_class_name = PlexAPIServiceThreadExecutor.__name__
                thread_executor = ThreadBatchExecutor(
                    scraped_medias, thread_class_name, plex_service, plex_service_function, source_service
                )
                plex_media_objs = thread_executor.start_threads_and_receive_result()
                plex_medias.extend(plex_media_objs)
                cached_items.extend(plex_media_objs)

        if plex_service.plex_playlist_exists(playlist_item.get_playlist_name()):
            plex_playlist = plex_service.fetch_plex_playlist_by_title(playlist_item.get_playlist_name())
            if not playlist_item.get_exact_sync():
                if len(plex_medias) > 0:
                    plex_media_items = [plex_media.get_media_item() for plex_media in plex_medias]
                    plex_playlist.addItems(plex_media_items)
            else:
                plex_service.delete_plex_playlist(plex_playlist)
                if len(plex_medias) > 0:
                    plex_media_items = [plex_media.get_media_item() for plex_media in plex_medias]
                    plex_service.create_playlist(playlist_item.get_playlist_name(), plex_media_items)
        else:
            if len(plex_medias) > 0:
                plex_playlist = plex_service.create_playlist(
                    playlist_item.get_playlist_name(), [plex_media.get_media_item() for plex_media in plex_medias]
                )
        print(str(len(plex_medias)) + " was added and it took: " + str(time.time() - start_time))
except Exception as e:
    # TODO: Implement better exception handling for main methods and internal methods
    print(e)
