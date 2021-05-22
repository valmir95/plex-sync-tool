import math
from service.thread_executor.PlexAPIServiceThreadExecutor import PlexAPIServiceThreadExecutor


class ThreadBatchExecutor(object):
    def __init__(self, items, thread_class_name, call_class_instance, call_function, source_service) -> None:
        self.items = items
        self.thread_class_name = thread_class_name
        self.call_class_instance = call_class_instance
        self.call_function = call_function
        self.source_service = source_service

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

    def start_threads_and_receive_result(self, batch_size=None):
        if not batch_size:
            batch_size = self.get_balanced_batch_size()
        batches = self.get_batches_of_items(batch_size)
        print("Running " + str(len(batches)) + " threads with a length of " + str(batch_size) + " items per batch")
        threads = []
        result = []
        for batch in batches:
            try:
                t_class = globals()[self.thread_class_name](
                    self.call_class_instance, batch, self.call_function, self.source_service
                )
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

    def get_balanced_batch_size(self):
        batch_size = 10
        if len(self.items) <= 50:
            batch_size = 2
        elif len(self.items) > 50 and len(self.items) < 80:
            batch_size = 6
        elif len(self.items) > 80 and len(self.items) < 120:
            batch_size = 8

        return batch_size
