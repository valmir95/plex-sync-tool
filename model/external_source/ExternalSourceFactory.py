from model.external_source.ImdbExternalSource import ImdbExternalSource
from model.external_source.TmdbExternalSource import TmdbExternalSource
from model.external_source.TraktExternalSource import TraktExternalSource


class ExternalSourceFactory(object):
    def __init__(self, source_type) -> None:
        self.source_type = source_type

    def get_external_source(self):
        source_type_str = self.source_type.value.lower().split(".")[0]
        external_source_class_name = source_type_str.capitalize() + "ExternalSource"
        external_source = globals()[external_source_class_name]()
        return external_source