# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = ['PoolExecutorAddon']

from typing import Optional
from concurrent.futures import Future, Executor


class PoolExecutorAddon:

    def __init__(self):
        from ..futures.executors import PoolExecutor
        self.executor: Optional[PoolExecutor] = None

    def before_start(self) -> None:
        pass

    def on_start(self) -> None:
        pass

    def initializer(self) -> None:
        pass

    def before_submit(self) -> None:
        pass

    def after_submit(self, future: Future) -> None:
        pass

    def before_join(self) -> None:
        pass

    def after_join(self) -> None:
        pass

    def after_shutdown(self) -> None:
        pass

    def __getstate__(self):
        state = {k: v for k, v in self.__dict__.items() if k != 'executor'}
        state['executor'] = None
        return state

    def __setstate__(self, state):
        state = state.copy()
        state['executor'] = None
        self.__dict__.update(state)

