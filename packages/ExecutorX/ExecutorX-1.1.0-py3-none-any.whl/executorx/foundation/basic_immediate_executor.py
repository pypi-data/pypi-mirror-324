# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = [
    'BasicImmediateExecutor', 'ImmediateFuture'
]


import concurrent.futures


class BasicImmediateExecutor(concurrent.futures.Executor):
    def __init__(self, max_worker=None, second_arg=None, initializer=None, initargs=(), **kwargs):
        self.initializer = initializer
        self.initargs = initargs
        self.initialized = False
        super().__init__()

    def submit(self, fn, *args, **kwargs):
        if not self.initialized:
            if self.initializer is not None:
                self.initializer(*self.initargs)
            self.initialized = True
        try:
            result = fn(*args, **kwargs)
            future = ImmediateFuture()
            future.set_result(result)
        except Exception as e:
            future = ImmediateFuture()
            future.set_exception(e)
        return future

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        for args in zip(*iterables):
            yield self.submit(fn, *args).result(timeout=timeout)

    def shutdown(self, wait=True, *, cancel_futures=False):
        pass


class ImmediateFuture(concurrent.futures.Future):
    def __init__(self):
        super().__init__()

    def cancel(self):
        return False

    def cancelled(self):
        return False

    def running(self):
        return False

    def done(self):
        return True

    def result(self, timeout=None):
        if self._state == concurrent.futures._base.CANCELLED:
            raise concurrent.futures.CancelledError()
        elif self._state == concurrent.futures._base.FINISHED:
            if self._exception:
                raise self._exception
            return self._result
        else:
            raise concurrent.futures.TimeoutError()

    def exception(self, timeout=None):
        if self._state == concurrent.futures._base.CANCELLED:
            raise concurrent.futures.CancelledError()
        elif self._state == concurrent.futures._base.FINISHED:
            return self._exception
        else:
            raise concurrent.futures.TimeoutError()

    def add_done_callback(self, fn):
        fn(self)
