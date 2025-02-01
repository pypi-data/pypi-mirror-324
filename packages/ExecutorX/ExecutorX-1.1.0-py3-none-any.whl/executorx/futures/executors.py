# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']


import concurrent.futures as cf
import functools
import inspect
import multiprocessing as mp
import uuid
from collections import deque

from .. import threading
from typing import Union, Optional, Iterable, Callable, List, Dict, Type
import weakref
from ..foundation.addon import PoolExecutorAddon
from ..foundation.executor_identifier import (
    FuncWrapperWithExecutorIdentifier,
    set_current_executor_identifier
)
from ..foundation.basic_immediate_executor import BasicImmediateExecutor
from ..utils import timeout_context_for_lock

__author_ = 'Yuting Zhang'

__all__ = [
    'BasicImmediateExecutor',
    'PoolExecutor',
]


def canonicalize_max_workers(max_workers):
    if max_workers is None:
        return mp.cpu_count()
    elif max_workers <= -1:
        return max(0, int(mp.cpu_count() + max_workers))
    elif -1 <= max_workers < 0:
        return max(0, int(mp.cpu_count() * (1 + max_workers)))
    elif 0 < max_workers < 1:
        return int(mp.cpu_count() * max_workers)
    else:
        return int(max_workers)


def create_basic_pool_executor(
        max_workers=None, *args,
        thread_instead_of_process: bool = False,
        **kwargs,
):
    max_workers = canonicalize_max_workers(max_workers)
    if max_workers == 0:
        et = BasicImmediateExecutor
    elif thread_instead_of_process:
        et = cf.ThreadPoolExecutor
    else:
        et = cf.ProcessPoolExecutor

    executor = et(max_workers, *args, **kwargs)
    return executor


class _FuncWithPreFuncs:
    def __init__(self, *args):
        self.functions = list(args)

    def __call__(self, *args, **kwargs):
        if not self.functions:
            return
        for fn in self.functions[:-1]:
            fn()
        self.functions[-1](*args, **kwargs)


class _TaskTracker:
    def __init__(self):
        self.op_rlock = threading.RLock()
        self.pending_futures: Dict[int, cf.Future] = dict()
        self.total_task_count = 0
        self.joined_lock = threading.Lock()

    @property
    def pending_total_task_count(self) -> int:
        with self.op_rlock:
            return len(self.pending_futures)

    def after_submit(self, future: cf.Future):
        with self.op_rlock:
            self.joined_lock.acquire(blocking=False)
            task_id = self.total_task_count
            self.pending_futures[task_id] = future
            self.total_task_count += 1
        # do not put the add_done_callback in the op_rlock context
        # when the task is done fast, the done callback may be triggered right away,
        # which will cause deadlock on op_rlock
        future.add_done_callback(functools.partial(self.task_done_callback, task_id=task_id))

    def task_done_callback(self, future: cf.Future, task_id: int):
        with self.op_rlock:
            self.pending_futures.pop(task_id)
            if not self.pending_futures:
                self.joined_lock.release()

    def join(self, timeout=None):
        with timeout_context_for_lock(self.joined_lock, timeout=timeout):
            pass


_ADDON_ARG_TYPE_HINT = Optional[
    Union[
        PoolExecutorAddon, Type[PoolExecutorAddon],
        Iterable[Union[PoolExecutorAddon,Type[PoolExecutorAddon]]],
    ]
]


class PoolExecutor(cf.Executor):

    def __init__(
            self, max_workers=None,
            initializer=None, initargs=(),
            thread_instead_of_process: bool = False,
            addons: _ADDON_ARG_TYPE_HINT = None,
            **kwargs,
    ):
        self.identifier = uuid.uuid4().hex

        self._max_workers = canonicalize_max_workers(max_workers)
        self.initializer = initializer
        self.thread_instead_of_process = thread_instead_of_process

        if addons is None:
            addons = []
        elif isinstance(addons, PoolExecutorAddon) or inspect.isclass(addons):
            addons = [addons]
        addons = list(
            (ao() if inspect.isclass(ao) else ao) for ao in addons
        )
        self.addons: List[PoolExecutorAddon] = addons

        for ao in self.addons:
            ao.executor = weakref.proxy(self)
            with set_current_executor_identifier(self.identifier):
                ao.before_start()

        self._task_tracker = _TaskTracker()
        self._submit_lock = threading.Lock()

        if addons:
            all_initializers = tuple(ao.initializer for ao in addons)
            if initializer is not None:
                all_initializers += (initializer,)
            initializer = FuncWrapperWithExecutorIdentifier(
                _FuncWithPreFuncs(*all_initializers), self.identifier
            )

        self._basic_executor = create_basic_pool_executor(
            max_workers, thread_instead_of_process=thread_instead_of_process,
            initializer=initializer, initargs=initargs,
            **kwargs
        )

        with set_current_executor_identifier(self.identifier):
            for ao in self.addons:
                ao.on_start()
        self.is_running = True

    @property
    def max_workers(self) -> int:
        return self._max_workers

    @property
    def task_op_rlock(self):
        return self._task_tracker.op_rlock

    @property
    def pending_total_task_count(self) -> int:
        return self._task_tracker.pending_total_task_count

    @property
    def total_task_count(self) -> int:
        return self._task_tracker.total_task_count

    @property
    def is_thread_pool(self) -> bool:
        return (
            isinstance(self.basic_executor, cf.ThreadPoolExecutor)
        )

    @property
    def is_process_pool_fork(self) -> bool:
        return (
            isinstance(self.basic_executor, cf.ProcessPoolExecutor) and
            isinstance(self.basic_executor._mp_context, mp.context.ForkContext)
        )

    @property
    def is_process_pool_spawn(self) -> bool:
        return (
            isinstance(self.basic_executor, cf.ProcessPoolExecutor) and
            isinstance(self.basic_executor._mp_context, mp.context.SpawnContext)
        )

    @property
    def basic_executor(self) -> cf.Executor:
        return self._basic_executor

    def submit(self, fn: Callable, /, *args, **kwargs) -> cf.Future:
        with self._submit_lock:
            with set_current_executor_identifier(self.identifier):
                for ao in self.addons:
                    ao.before_submit()
            wrapped_fn = FuncWrapperWithExecutorIdentifier(fn, self.identifier)
            f = self._basic_executor.submit(
                wrapped_fn, *args, **kwargs
            )
            self._task_tracker.after_submit(f)
            with set_current_executor_identifier(self.identifier):
                for ao in self.addons[::-1]:
                    ao.after_submit(f)
            return f

    def basic_submit(self, fn: Callable, /, *args, **kwargs) -> cf.Future:
        return self._basic_executor.submit(fn, *args, **kwargs)

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        assert timeout is None, 'timeout is not supported for now'  # FIXME
        assert chunksize == 1, 'chunksize must be 1 for now'  # FIXME
        futures = deque(self.submit(fn, *i) for i in zip(*iterables))
        for f in futures:
            yield f.result()
        # return self._basic_executor.map(fn, *iterables, timeout=timeout, chunksize=chunksize)

    def shutdown(self, wait=True, **kwargs):
        if 'is_running' not in self.__dict__ or not self.is_running:
            return
        rt = self._basic_executor.shutdown(wait=True, **kwargs)
        self.join()
        self.is_running = False
        with set_current_executor_identifier(self.identifier):
            for ao in self.addons:
                ao.after_shutdown()
        return rt

    def join(self, timeout=None):
        with set_current_executor_identifier(self.identifier):
            for ao in self.addons:
                ao.before_join()
        self._task_tracker.join(timeout=timeout)
        with set_current_executor_identifier(self.identifier):
            for ao in self.addons:
                ao.after_join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False

    def __del__(self):
        self.shutdown(wait=True)


class ImmediateExecutor(PoolExecutor):

    def __init__(
            self,
            initializer=None, initargs=(),
            addons: _ADDON_ARG_TYPE_HINT = None,
    ):
        super().__init__(
            max_workers=0,
            initializer=initializer, initargs=initargs,
            thread_instead_of_process=False, addons=addons,
        )


class ProcessPoolExecutor(PoolExecutor):

    def __init__(
            self,
            max_workers=None, mp_context=None,
            initializer=None, initargs=(),
            addons: _ADDON_ARG_TYPE_HINT = None,
    ):
        super().__init__(
            max_workers=max_workers, mp_context=mp_context,
            initializer=initializer, initargs=initargs,
            thread_instead_of_process=False, addons=addons,
        )


class ThreadPoolExecutor(PoolExecutor):

    def __init__(
            self,
            max_workers=None, thread_name_prefix='',
            initializer=None, initargs=(),
            addons: _ADDON_ARG_TYPE_HINT = None,
    ):
        super().__init__(
            max_workers=max_workers,
            thread_name_prefix=thread_name_prefix,
            initializer=initializer, initargs=initargs,
            thread_instead_of_process=True, addons=addons,
        )
