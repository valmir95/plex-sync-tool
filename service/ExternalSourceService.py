class ExternalSourceService(object):
    def __init__(self, external_source):
        self.external_source = external_source

    def get_media_from_external_playlist(self):
        raise Exception("Method not implemented")

    def get_external_source(self):
        return self.external_source

    def set_external_source(self, external_source):
        self.external_source = external_source
