from model.external_source.enum.ExternalSourceType import ExternalSourceType


class PlexGuid(object):
    def __init__(self, guid_id, source_type) -> None:
        super().__init__()
        self.guid_id = guid_id
        self.source_type = source_type

    def get_guid_id(self):
        return self.guid_id

    def get_source_type(self):
        return self.source_type

    def set_guid_id(self, guid_id):
        self.guid_id = guid_id

    def set_source_type(self, source_type):
        self.source_type = source_type

    @staticmethod
    def create_from_str(guid_str):
        guid_split = guid_str.split("://")
        if len(guid_split) == 2:
            source_type = ExternalSourceType[guid_split[0].upper()]
            guid_id = guid_split[1]
            return PlexGuid(guid_id, source_type)
        raise Exception("There was something wrong with the guid string")
