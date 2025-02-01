# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = [
    'VarRegistry'
]


from uuid import uuid4
from ..futures.addon import PoolExecutorAddon

_worker_ids = dict()


current_session = None
var_registry = dict()


def current_var_registry():
    global current_session, var_registry
    if current_session not in var_registry:
        return dict()
    return var_registry[current_session]


def get_var(key):
    return current_var_registry().get(key)

class VarRegistry(PoolExecutorAddon):

    def __init__(self, var_dict: dict = None, /, **kwargs):
        super().__init__()
        if var_dict is None:
            var_dict = {}
        self.var_dict = {**var_dict, **kwargs}

    @classmethod
    def get(cls, key):
        return get_var(key)

    def initializer(self) -> None:
        global current_session, var_registry
        if not current_session:
            current_session = uuid4().hex
        if current_session not in var_registry:
            var_registry[current_session] = self.var_dict

    def after_shutdown(self) -> None:
        # clean up if in main thread
        global current_session, var_registry
        if current_session in var_registry:
            try:
                del var_registry[current_session]
            except KeyError:
                pass
