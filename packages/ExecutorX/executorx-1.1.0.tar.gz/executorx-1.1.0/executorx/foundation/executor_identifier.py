__all__ = [
    'get_current_executor_identifier',
    'set_current_executor_identifier',
    'FuncWrapperWithExecutorIdentifier'
]


from collections import defaultdict
import contextlib
import os
import threading

current_executor_identifier = defaultdict(lambda: None)

_identifier_lock = threading.Lock()


def _get_worker_identifier():
    return os.getpid(), threading.get_ident()


def get_current_executor_identifier():
    with _identifier_lock:
        return current_executor_identifier[_get_worker_identifier()]


@contextlib.contextmanager
def set_current_executor_identifier(executor_identifier):
    global current_executor_identifier
    with _identifier_lock:
        worker_identifier = _get_worker_identifier()
        previous_executor_identifier = current_executor_identifier[worker_identifier]
        current_executor_identifier[worker_identifier] = executor_identifier
    yield
    with _identifier_lock:
        current_executor_identifier[worker_identifier] = previous_executor_identifier
        if current_executor_identifier[worker_identifier] is None:
            current_executor_identifier.pop(worker_identifier)


class FuncWrapperWithExecutorIdentifier:
    def __init__(self, func, executor_identifier):
        self.func = func
        self.executor_identifier = executor_identifier

    def __call__(self, *args, **kwargs):
        with set_current_executor_identifier(self.executor_identifier):
            return self.func(*args, **kwargs)
