from model.external_source.ExternalSourceFactory import ExternalSourceFactory
from service.external_source.ImdbSourceService import ImdbSourceService
from service.external_source.TmdbSourceService import TmdbSourceService
from model.external_source.ImdbExternalSource import ImdbExternalSource
from model.external_source.TmdbExternalSource import TmdbExternalSource


class SourceServiceFactory(object):
    def __init__(self, source_type, config) -> None:
        self.source_type = source_type
        self.config = config

    def get_source_service(self):
        external_source_factory = ExternalSourceFactory(self.source_type, self.config)
        external_source = external_source_factory.get_external_source()
        source_type_str = self.source_type.value.lower()
        source_service_class_name = source_type_str.capitalize() + "SourceService"
        source_service = globals()[source_service_class_name](external_source, self.config, self.source_type)
        return source_service