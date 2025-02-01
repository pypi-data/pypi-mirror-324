# Author: Yuting Zhang
# This file is part of ExecutorX, licensed under the GNU Lesser General Public License V2.1.

__author__ = ['Yuting Zhang']

__all__ = ['start_all_workers']

import concurrent.futures as cf
import multiprocessing as mp
import multiprocessing.managers as mpm
from ..futures import PoolExecutor


def _start_barrier(barrier):
    barrier.wait()


def start_all_workers(executor: PoolExecutor):
    max_workers = executor.max_workers
    if not max_workers or max_workers < 0:
        return
    if executor.is_process_pool_spawn:
        manager = mpm.SyncManager()
        manager.start()
        barrier = manager.Barrier(max_workers)
    else:
        # FIXME: this may be problematic if some workers are started already
        manager = None
        barrier = mp.Barrier(max_workers)
    all_tasks = {executor.basic_submit(_start_barrier, barrier) for _ in range(max_workers)}
    for _ in cf.as_completed(all_tasks):
        pass
    if manager is not None:
        manager.shutdown()
        del manager
