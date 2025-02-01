# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = ['Progress']

from .. import threading
from concurrent.futures import Future
import concurrent.futures as cf
from typing import Optional
from executorx.foundation.addon import PoolExecutorAddon
from ..futures.executors import BasicImmediateExecutor


class Progress(PoolExecutorAddon):
    def __init__(
            self,
            num_tasks: Optional[int] = None,
            desc: Optional[str] = None,
            reset_at_join: bool = True,
            show_title: bool = True,
    ):
        try:
            from tqdm.auto import tqdm
        except ImportError:
            raise ImportError('tqdm is needed to use Progress. use pip install tqdm to install.')

        super().__init__()
        self.show_title = show_title
        self.reset_at_join = reset_at_join
        self.op_rlock = threading.RLock()
        self.reset(num_tasks=num_tasks, desc=desc)
        self.submitted_num_tasks = 0

    def reset(self, num_tasks: Optional[int] = None, desc: Optional[str] = None):
        if hasattr(self, '_pbar') and self._pbar is not None:
            self._pbar.close()
        with self.op_rlock:
            self.submitted_num_tasks = 0
            self.num_tasks = num_tasks
            self.done_tasks = 0
            self.complete_tasks = 0
            self.failed_tasks = 0
            self.canceled_tasks = 0
            self.desc = desc
            self._pbar = None

    @property
    def pbar(self):
        with self.op_rlock:
            if self._pbar is None:
                from tqdm.auto import tqdm
                self._pbar = tqdm(total=self.num_tasks, desc=self.desc)
            return self._pbar

    def task_done_callback(self, future: Future):
        is_problematic = False
        self.done_tasks += 1
        if future.cancelled():
            self.canceled_tasks += 1
            is_problematic = True
        elif future.exception() is not None:
            self.failed_tasks += 1
            is_problematic = True
        else:
            self.complete_tasks += 1
        if is_problematic:
            additional_info = dict()
            if self.canceled_tasks:
                additional_info['canceled'] = self.canceled_tasks
            if self.failed_tasks:
                additional_info['failed'] = self.failed_tasks
            self.pbar.set_postfix(additional_info)
        self.pbar.update(1)

    def on_start(self) -> None:

        if not self.show_title:
            return

        if isinstance(self.executor.basic_executor, BasicImmediateExecutor):
            worker_info = 'main thread'
        elif isinstance(self.executor.basic_executor, cf.ProcessPoolExecutor):
            worker_info = f'{self.executor.max_workers} processes'
        elif isinstance(self.executor.basic_executor, cf.ThreadPoolExecutor):
            worker_info = f'{self.executor.max_workers} thread'
        else:
            worker_info = None
        title = f"Run '{self.desc}' " if self.desc else 'Run '
        if worker_info:
            title += f"on {worker_info}"
        else:
            title += 'with an executor'
        print(title, flush=True)

    def after_submit(self, future: Future) -> None:
        future.add_done_callback(self.task_done_callback)
        self.submitted_num_tasks += 1

    def before_join(self) -> None:
        if not self.num_tasks:
            self.pbar.total = self.submitted_num_tasks
            self.pbar.refresh()

    def after_join(self) -> None:
        if (
                hasattr(self, 'reset_at_join') and self.reset_at_join and
                hasattr(self, '_pbar') and self._pbar is not None
        ):
            self.reset()
