class PlexMediaItem(object):
    def __init__(self, media_item, list_url, media_id) -> None:
        self.media_item = media_item
        self.list_url = list_url
        self.media_id = media_id

    def get_media_item(self):
        return self.media_item

    def get_list_url(self):
        return self.list_url

    def get_media_id(self):
        return self.media_id
