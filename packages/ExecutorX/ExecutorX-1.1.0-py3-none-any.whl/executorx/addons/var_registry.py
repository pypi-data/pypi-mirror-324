# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = [
    'VarRegistry'
]


from executorx.foundation.addon import PoolExecutorAddon
from executorx.foundation.executor_identifier import get_current_executor_identifier


class _VarRegistry:
    val = dict()


def get_var_registry():
    return _VarRegistry.val


def current_var_registry():
    current_executor_id = get_current_executor_identifier()
    if current_executor_id not in get_var_registry():
        return dict()
    return get_var_registry()[current_executor_id]


def get_var(key):
    return current_var_registry().get(key)

class VarRegistry(PoolExecutorAddon):

    def __init__(self, var_dict: dict = None, /, **kwargs):
        super().__init__()
        if var_dict is None:
            var_dict = {}
        self.var_dict = {**var_dict, **kwargs}
        self.need_to_pickle_var_dict = True

    @classmethod
    def get(cls, key):
        return get_var(key)

    def on_start(self) -> None:
        if not self.executor.is_process_pool_spawn:
            self.need_to_pickle_var_dict = False
            get_var_registry()[get_current_executor_identifier()] = dict(self.var_dict)

    def initializer(self) -> None:
        executor_id = get_current_executor_identifier()
        if executor_id not in get_var_registry():
            get_var_registry()[executor_id] = dict(self.var_dict)

    def after_shutdown(self) -> None:
        # clean up if in main thread
        executor_id = get_current_executor_identifier()
        if executor_id in get_var_registry():
            try:
                del get_var_registry()[executor_id]
            except KeyError:
                pass

    def __getstate__(self):
        d = super().__getstate__()
        if not self.need_to_pickle_var_dict:
            d['var_dict'] = None
        return d
