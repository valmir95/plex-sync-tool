import threading
import time


class PlexAPIThread(threading.Thread):
    def __init__(self, plex_service, plex_media_item_batch):
        threading.Thread.__init__(self)
        self.plex_service = plex_service
        self.plex_media_item_batch = plex_media_item_batch
        self.plex_media_items_result = []

    def run(self):
        plex_media_objs = self.plex_service.get_plex_media_objs_from_external_media_objs(self.plex_media_item_batch)
        self.plex_media_items_result.extend(plex_media_objs)

    def get_plex_service(self):
        return self.plex_service

    def get_plex_media_items_result(self):
        return self.plex_media_items_result

    def get_plex_media_item_batch(self):
        return self.plex_media_item_batch
