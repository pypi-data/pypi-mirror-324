# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = [
    'my_worker_id',
    'WorkerId',
]


import multiprocessing
import os
from .. import threading
from executorx.foundation.addon import PoolExecutorAddon

_worker_ids = dict()


def _get_worker_identifier():
    return os.getpid(), threading.get_ident()


def my_worker_id():
    global _worker_ids
    my_worker_identifier = _get_worker_identifier()
    if my_worker_identifier in _worker_ids:
        return _worker_ids[my_worker_identifier]
    return None


class WorkerId(PoolExecutorAddon):

    @staticmethod
    def my_worker_id():
        return my_worker_id()

    def __init__(self):
        super().__init__()
        self._lock = multiprocessing.Lock()
        self._counter = multiprocessing.Value('i', 0)
        self.max_workers = 0

    def before_start(self) -> None:
        self.max_workers = self.executor.max_workers

    @property
    def total_started_workers(self) -> int:
        with self._lock:
            return self._counter.value

    def initializer(self) -> None:
        if not self.max_workers:
             return
        with self._lock:
            my_worker_id = self._counter.value
            self._counter.value += 1
        global _worker_ids
        _worker_ids[_get_worker_identifier()] = my_worker_id

