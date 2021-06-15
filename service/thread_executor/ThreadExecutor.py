import threading


class ThreadExecutor(threading.Thread):
    def __init__(self, call_class_instance, item_batch, call_class_function_name, source_service) -> None:
        threading.Thread.__init__(self)
        self.call_class_instance = call_class_instance
        self.item_batch = item_batch
        self.call_class_function_name = call_class_function_name
        self.thread_result = []
        self.source_service = source_service

    def run(self) -> None:
        raise Exception("Not implemented")

    def get_call_class_instance(self):
        return self.call_class_instance

    def get_item_batch(self):
        return self.item_batch

    def get_call_class_function_name(self):
        return self.call_class_function_name

    def get_thread_result(self):
        return self.thread_result

    def get_source_service(self):
        return self.source_service