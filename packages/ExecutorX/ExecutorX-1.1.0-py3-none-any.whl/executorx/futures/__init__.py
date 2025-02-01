# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

"""
Expanding `current.futures` capacity with
1. BasicImmediateExecutor for running tasks in the main process/thread under the same executor interface.
2. max_worker=0 to use BasicImmediateExecutor in ProcessPoolExecutor / ThreadPoolExecutor
3. support of extensions to add initializers and process futures
"""

__author__ = ['Yuting Zhang']


import concurrent.futures as _concurrent_futures

from concurrent.futures import *
BasicProcessPoolExecutor = ProcessPoolExecutor
BasicThreadPoolExecutor = ThreadPoolExecutor
from .executors import *
from .executors import ProcessPoolExecutor, ThreadPoolExecutor
from .start_all_workers import *


__all__ = tuple(_concurrent_futures.__all__) + (
    'BasicProcessPoolExecutor',
    'BasicThreadPoolExecutor',
    'BasicImmediateExecutor',
    'ImmediateFuture',
    'ImmediateExecutor',
    'PoolExecutor',
    'PoolExecutorAddon',
    'start_all_workers',
)
