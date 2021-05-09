class ExternalSourceMedia(object):
    def __init__(self, media_name, media_id, source_type, external_url=None, year=None) -> None:
        self.media_name = media_name
        self.media_id = media_id
        self.source_type = source_type
        self.external_url = external_url
        self.year = year

    def get_media_name(self):
        return self.media_name

    def get_media_id(self):
        return self.media_id

    def get_source_type(self):
        return self.source_type

    def get_external_url(self):
        return self.external_url

    def get_year(self):
        return self.year

    def set_media_name(self, media_name):
        self.media_name = media_name

    def set_media_id(self, media_id):
        self.media_id = media_id

    def set_source_type(self, source_type):
        self.source_type = source_type

    def set_external_url(self, external_url):
        self.external_url = external_url

    def set_year(self, year):
        self.year = year
