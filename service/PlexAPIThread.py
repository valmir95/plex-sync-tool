import threading
import time
from service.PlexAPIService import PlexAPIService


class PlexAPIThread(threading.Thread):
    def __init__(self, plex_service, plex_media_item_batch, plex_service_function):
        threading.Thread.__init__(self)
        self.plex_service = plex_service
        self.plex_media_item_batch = plex_media_item_batch
        self.thread_result = []
        self.plex_service_function = plex_service_function

    def run(self):

        plex_service_class_name = self.plex_service.__class__
        function_exists = hasattr(PlexAPIService, self.plex_service_function) and callable(
            getattr(PlexAPIService, self.plex_service_function)
        )
        plex_media_objs = getattr(self.plex_service, self.plex_service_function)(self.plex_media_item_batch)
        self.thread_result.extend(plex_media_objs)

        # plex_media_objs = self.plex_service.get_plex_media_objs_from_external_media_objs(self.plex_media_item_batch)

    def get_plex_service(self):
        return self.plex_service

    def get_thread_result(self):
        return self.thread_result

    def get_plex_media_item_batch(self):
        return self.plex_media_item_batch

    def get_plex_service_function(self):
        return self.plex_service_function
