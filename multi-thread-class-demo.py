from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time
from random import randint
import threading


class MyThreadingClass(object):
    """
        MyThreadingClass creates an instance of a thread using ThreadPoolExecutor.
    """
    def __init__(self):
        self.tp = ThreadPoolExecutor(max_workers=1)  # 1 thread per instance

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        # when wait=False, return immediately and the resources associated with the executor
        # will be freed when all pending futures are done executing.
        self.tp.shutdown(wait=False)

    def work(self, fn, arg):
        future = self.tp.submit(fn, arg)
        future.add_done_callback(self.done)

    def sleep(self, arg):
        time.sleep(arg)
        return arg

    def get_current_thread_native_id(self):
        # thread ID of this thread
        return threading.current_thread().native_id

    def done(self, future):
        print(future.result())
        print('native id: ' + str(self.get_current_thread_native_id()))
        print()


if __name__ == "__main__":
    for i in range(5):
        my_class = MyThreadingClass()
        with my_class as mc:
            mc.work(mc.sleep, randint(1, 5))
