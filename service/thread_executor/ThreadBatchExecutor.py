import math
from service.thread_executor.PlexAPIServiceThreadExecutor import PlexAPIServiceThreadExecutor


class ThreadBatchExecutor(object):
    def __init__(self, items, thread_class_name, call_class_instance, call_function) -> None:
        self.items = items
        self.thread_class_name = thread_class_name
        self.call_class_instance = call_class_instance
        self.call_function = call_function

    def get_batches_of_items(self, size_per_batch):
        if size_per_batch >= len(self.items):
            return [self.items]
        batches = []
        start = 0
        end = size_per_batch
        last_index = 0
        for i in range(int(len(self.items) / size_per_batch)):
            media_batch = []
            for j in range(start, end):
                if len(self.items) > j:
                    media_batch.append(self.items[j])
                    last_index = j
            batches.append(media_batch)
            start += size_per_batch
            end += size_per_batch

        remainder = (len(self.items) - last_index) - 1
        if remainder > 0:
            start = int(len(self.items)) - remainder
            end = start + remainder
            media_batch = []
            for i in range(start, end):
                media_batch.append(self.items[i])
            batches.append(media_batch)

        return batches

    def start_threads_and_receive_result(self, items_per_thread):
        batches = self.get_batches_of_items(items_per_thread)
        threads = []
        result = []
        for batch in batches:
            try:
                t_class = globals()[self.thread_class_name](self.call_class_instance, batch, self.call_function)
            except:
                raise Exception(
                    "Could not initiate/find ThreadExecutor subclass: '"
                    + self.thread_class_name
                    + "'. Class and/or function most likely cannot be found."
                )
            threads.append(t_class)
            t_class.start()

        for thread in threads:
            thread.join()
            result.extend(thread.get_thread_result())

        return result


def create_threads(medias, plex_service, plex_service_function):
    floored_count = math.floor(len(medias) / 10) * 10
    remainder = len(medias) - floored_count
    thread_count = int(floored_count / 10)
    plex_api_threads = []
    start = 0
    end = 10
    result = []
    for t in range(thread_count):
        media_batch = []
        for i in range(start, end):
            media_batch.append(medias[i])
        plex_api_threads.append(PlexAPIThread(plex_service, media_batch, plex_service_function))
        start += 10
        end += 10
    if remainder > 0:
        start = int(len(medias)) - remainder
        end = start + remainder
        batch = []
        for i in range(start, end):
            batch.append(medias[i])
        plex_api_threads.append(PlexAPIThread(plex_service, batch, plex_service_function))

    for plex_thread in plex_api_threads:
        plex_thread.start()

    for plex_thread in plex_api_threads:
        plex_thread.join()
        result.extend(plex_thread.get_plex_media_items_result())

    print("ALL THREADS FINISHED!")

    return result