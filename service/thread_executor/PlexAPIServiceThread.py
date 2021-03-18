from service.thread_executor.ThreadExecutor import ThreadExecutor
from service.plex.PlexAPIService import PlexAPIService


class PlexAPIServiceThread(ThreadExecutor):
    def __init__(self, call_class_instance, item_batch, call_class_function_name):
        super().__init__(call_class_instance, item_batch, call_class_function_name)

    def run(self):
        has_function = hasattr(PlexAPIService, self.call_class_function_name)
        function_callable = callable(getattr(PlexAPIService, self.call_class_function_name))

        function_exists = has_function and function_callable
        if function_exists:
            plex_media_objs = getattr(self.call_class_instance, self.call_class_function_name)(self.item_batch)
            self.thread_result.extend(plex_media_objs)
        else:
            raise Exception(
                "Function '"
                + self.call_class_function_name
                + " could not be found in '"
                + self.call_class_instance.__name__
                + "'"
            )
