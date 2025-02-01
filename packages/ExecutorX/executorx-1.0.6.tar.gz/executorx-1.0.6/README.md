
# ExecutorX

[![License](https://img.shields.io/badge/License-LGPLv2.1-blue.svg)](LICENSE)

**ExecutorX** is an advanced executor library for Python that extends `concurrent.futures.Executor` with new capabilities, including task progress tracking, submission throttling, modular lifecycle hooks, and improved support for worker initialization. Whether you're running CPU-bound tasks in processes, IO-bound tasks in threads, or debugging in the main thread, **ExecutorX** makes parallelism more flexible and powerful.

---

## Features

### Enhanced Executors
- **ProcessPoolExecutor** and **ThreadPoolExecutor**:
  - Advanced executors with support for addons, task tracking, and flexible worker initialization.
- **ImmediateExecutor**:
  - Executes tasks in the main thread synchronously for debugging and testing.

### Advanced Features
1. **Progress Tracking**: Monitor task completion and pending tasks in real time.
2. **Submission Throttling**: Limit the number of concurrent tasks or submission rate to prevent overloading workers.
3. **Worker Initialization**: Define custom initialization logic for workers (e.g., resource setup).
4. **Worker Identification**: Assign and track unique worker IDs.
5. **Lifecycle Addons**: Extend executor behavior with modular addons for logging, monitoring, or custom task logic.

### Utilities
- **Support for `spawn` Context**:
  - Ensures compatibility with platforms like Windows, which lack support for the `fork` multiprocessing context.
- **Graceful Shutdown**:
  - Ensures all tasks complete before the executor shuts down, even when using custom addons.

---

## Installation

```bash
pip install ExecutorX
```

---

## Quick Start

### Process Pool with Progress Tracking

```python
from executorx.addons.progress import ProgressAddon
from executorx.futures.executors import ProcessPoolExecutor


def my_function(x):
    return x * x


# Initialize a process pool with progress tracking
executor = ProcessPoolExecutor(max_workers=4, addons=[ProgressAddon])

# Submit tasks
futures = [executor.submit(my_function, i) for i in range(10)]

# Collect results
for future in futures:
    print(future.result())

executor.shutdown()
```

### Immediate Execution Mode (Single-Threaded)

The `ImmediateExecutor` runs all tasks in the main thread synchronously. This is useful for debugging or environments where parallelism isn't required.

```python
from executorx.futures.executors import ImmediateExecutor


def debug_task(x):
    print(f"Processing {x} in the main thread")
    return x * x


executor = ImmediateExecutor()

# Submit tasks
futures = [executor.submit(debug_task, i) for i in range(5)]

# Collect results
for future in futures:
    print(future.result())

executor.shutdown()
```

### Throttling Task Submissions

Control the number of concurrent or submitted tasks using the `ThrottleAddon`.

```python
from executorx.addons.throttle import ThrottleAddon
from executorx.futures.executors import ThreadPoolExecutor

executor = ThreadPoolExecutor(
    max_workers=4, addons=[ThrottleAddon(max_concurrent_tasks=2)]
)

# Submit tasks (at most 2 will run concurrently)
futures = [executor.submit(print, f"Task {i}") for i in range(10)]

executor.shutdown()
```

### Worker Initialization

Set up custom initialization logic for workers, such as loading shared resources.

```python
from executorx.futures.executors import ProcessPoolExecutor


def initialize_worker():
    print("Initializing worker...")


executor = ProcessPoolExecutor(max_workers=4, initializer=initialize_worker)

executor.submit(print, "Task executed with worker initialization")
executor.shutdown()
```

---

## Addons: Extending Executors

Addons provide modular hooks into the executor lifecycle, allowing custom logic for task submission, initialization, and shutdown.

### Creating a Custom Addon

```python
from executorx.futures.addon import PoolExecutorAddon


class MyCustomAddon(PoolExecutorAddon):
    def before_submit(self):
        print("Preparing to submit task")

    def after_submit(self, future):
        print("Task submitted")


# Use the addon
from executorx.futures.executors import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4, addons=[MyCustomAddon])
executor.submit(print, "Hello from ExecutorX!")
executor.shutdown()
```

---

## Why ImmediateExecutor?

While setting `max_workers=0` in a process or thread pool allows single-threaded execution, **ImmediateExecutor** provides distinct advantages:

1. **Code Clarity**:
   - It explicitly communicates the intent to disable parallelism while keeping the API consistent with other executors.

2. **Debugging Support**:
   - Addons, worker initialization, and task tracking remain functional, making it easy to debug parallelized code in a single-threaded environment.

3. **Feature Parity**:
   - ImmediateExecutor retains all features of other executors (e.g., addons, lifecycle management), ensuring that testing environments mirror production.

---

## Contributing

Contributions are welcome! To get started:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add feature-name'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

---

## License

ExecutorX is licensed under the GNU Lesser General Public License (LGPL) v2.1. See the [LICENSE](LICENSE) file for details.

---

## Future Roadmap

- **Picklable Executors**: Allow executors to be serialized and passed across processes.

---
