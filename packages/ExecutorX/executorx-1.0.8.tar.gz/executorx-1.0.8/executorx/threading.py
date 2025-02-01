# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = [
    'RLock',
    'Lock',
]


from .utils import ResetAtPickleClassWrapper
import threading
from threading import *


class RLock(ResetAtPickleClassWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(threading.RLock, *args, **kwargs)

    def __enter__(self):
        self._initialize_if_needed()
        return self._obj.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._obj.__exit__(exc_type, exc_val, exc_tb)


class Lock(ResetAtPickleClassWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(threading.Lock, *args, **kwargs)

    def __enter__(self):
        self._initialize_if_needed()
        return self._obj.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._obj.__exit__(exc_type, exc_val, exc_tb)
