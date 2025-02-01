# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

from concurrent.futures import Future
from .. import threading
from typing import Union
from executorx.foundation.addon import PoolExecutorAddon


class Throttle(PoolExecutorAddon):
    def __init__(
            self,
            buffer_size: Union[int, None],
    ):
        super().__init__()
        if buffer_size is None or buffer_size <= 0:
            buffer_size = self.executor.max_workers * 8
        self.buffer_size = buffer_size
        self.throttle_lock = threading.Lock()

    def task_done_callback(self, future_obj, task_id: int):
        with self.executor.task_op_rlock:
            if self.executor.pending_task_count < self.buffer_size and not self.throttle_lock.acquire(blocking=False):
                self.throttle_lock.release()

    def before_submit(self) -> None:
        with self.throttle_lock:
            pass

    def after_submit(self, future: Future) -> None:
        with self.executor.task_op_rlock:
            if self.executor.pending_task_count >= self.buffer_size:
                self.throttle_lock.acquire(blocking=False)
        future.add_done_callback(self.task_done_callback)

