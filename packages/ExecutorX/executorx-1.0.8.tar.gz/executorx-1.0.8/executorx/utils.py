# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = [
    'timeout_context_for_lock',
    'ResetAtPickleClassWrapper',
]

import contextlib
import multiprocessing as mp
import threading
import typing


class ResetAtPickleClassWrapper:
    """
    A wrapper class that lazily initializes an object and resets its state during pickling.

    This wrapper allows deferred initialization of the wrapped object until an attribute
    or method is accessed. It also ensures that the wrapped object is reset (set to None)
    when pickled, making it useful for cases where the wrapped object cannot or should not
    be serialized directly.

    Attributes:
        _cls (type): The class of the object to be wrapped.
        _args (tuple): Positional arguments to pass to the constructor of the wrapped object.
        _kwargs (dict): Keyword arguments to pass to the constructor of the wrapped object.
        _obj (object or None): The lazily initialized wrapped object.
        _initialized (bool): A flag to indicate whether the wrapper has been fully initialized.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the wrapper with the class to be wrapped and its constructor arguments.

        Args:
            args: Positional arguments, where the first argument should be the class to wrap.
            kwargs: Keyword arguments for the constructor of the wrapped object.
        """
        self._cls = args[0]
        self._args = args[1:]
        self._kwargs = kwargs
        self._obj_holder = [None]
        self._initialized = True

    @property
    def _obj(self):
        return self._obj_holder[0]

    def _initialize_if_needed(self):
        if self._obj is None:
            self._obj_holder[0] = self._cls(*self._args, **self._kwargs)

    def __getattr__(self, item):
        """
        Lazily initialize the wrapped object and delegate attribute access to it.

        Args:
            item (str): The name of the attribute to access.

        Returns:
            The value of the attribute from the wrapped object.

        Raises:
            AttributeError: If the attribute does not exist in the wrapped object.
        """
        if '_initialized' not in self.__dict__ or not self._initialized:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")
        self._initialize_if_needed()
        return getattr(self._obj, item)

    def __setattr__(self, name, value):
        """
        Delegate attribute setting to the wrapped object if it exists, otherwise set on the wrapper.

        Args:
            name (str): The name of the attribute to set.
            value: The value to set the attribute to.
        """
        if '_initialized' not in self.__dict__ or not self._initialized:
            super().__setattr__(name, value)
            return
        self._initialize_if_needed()
        setattr(self._obj, name, value)

    def __getstate__(self):
        """
        Prepare the state of the wrapper for pickling.

        Returns:
            dict: A dictionary representing the state of the wrapper, with the wrapped object reset to None.
        """
        state = {k: v for k, v in self.__dict__.items() if k in {'_cls', '_args', '_kwargs'}}
        return state

    def __setstate__(self, state):
        """
        Restore the state of the wrapper after unpickling.

        Args:
            state (dict): A dictionary representing the state of the wrapper.
        """
        self.__dict__.update(state)
        self._obj_holder = [None]
        self._initialized = True


@contextlib.contextmanager
def timeout_context_for_lock(lock: typing.Union[threading.Lock, mp.Lock], timeout=None):
    if timeout is None:
        timeout = -1
    lock.acquire(timeout=timeout)
    yield lock
    lock.release()
