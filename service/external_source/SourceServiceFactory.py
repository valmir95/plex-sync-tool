from model.external_source.enum.ExternalSourceType import ExternalSourceType
from model.external_source.ExternalSource import ExternalSource
from model.external_source.ImdbExternalSource import ImdbExternalSource
from model.external_source.TmdbExternalSource import TmdbExternalSource
from model.external_source.TraktExternalSource import TraktExternalSource
from model.external_source.ExternalSourceFactory import ExternalSourceFactory
from service.external_source.SourceService import SourceService
from service.external_source.ImdbSourceService import ImdbSourceService
from service.external_source.TmdbSourceService import TmdbSourceService
from service.external_source.TraktSourceService import TraktSourceService


class SourceServiceFactory(object):
    def __init__(self, config) -> None:
        self.config = config

    def get_source_service_from_url(self, url) -> SourceService:
        source_type = self.get_source_type_from_url(url)
        external_source_factory = ExternalSourceFactory(source_type)
        external_source = external_source_factory.get_external_source()
        source_type_str = source_type.value.lower().split(".")[0]
        source_service_class_name = source_type_str.capitalize() + "SourceService"
        source_service = globals()[source_service_class_name](external_source, self.config, source_type)
        return source_service

    def get_source_type_from_url(self, url) -> ExternalSourceType:
        for sub_class in ExternalSource.__subclasses__():
            external_source = globals()[sub_class.__name__]()
            if external_source.get_source_type().value in url:
                return external_source.get_source_type()
        raise Exception("Service from " + str(url) + " is not yet supported.")
