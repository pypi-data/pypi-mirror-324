from __future__ import annotations

from threading import RLock
from rich import console
from rich_click import Command
import signal

import asyncio
import logging
import os
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures._base import Executor
from functools import lru_cache
from types import TracebackType
from typing_extensions import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Coroutine,
    Iterable,
    Literal,
    TypeVar,
    overload,
    Type,
)




from asyncio import events
from asyncio import exceptions
from asyncio import tasks
from rich.console import Console
console = Console()

import warnings

def smart_import(module_name: str):
    """Import a module and return it."""
    return __import__(module_name, fromlist=[""])

R = TypeVar("R")
T = TypeVar("T")
_AnyCallable = Callable[..., Any]
FC = TypeVar("FC", bound=_AnyCallable | Command)

def _set_task_name(task, name):
    if name is not None:
        try:
            set_name = task.set_name
        except AttributeError:
            warnings.warn("Task.set_name() was added in Python 3.8, "
                      "the method support will be mandatory for third-party "
                      "task implementations since 3.13.",
                      DeprecationWarning, stacklevel=3)
        else:
            set_name(name)



class TaskGroup:
    """Asynchronous context manager for managing groups of tasks.

    Example use:

        async with asyncio.TaskGroup() as group:
            task1 = group.create_task(some_coroutine(...))
            task2 = group.create_task(other_coroutine(...))
        print("Both tasks have completed now.")

    All tasks are awaited when the context manager exits.

    Any exceptions other than `asyncio.CancelledError` raised within
    a task will cancel all remaining tasks and wait for them to exit.
    The exceptions are then combined and raised as an `ExceptionGroup`.
    """
    def __init__(self):
        self._entered = False
        self._exiting = False
        self._aborting = False
        self._loop = None
        self._parent_task = None
        self._parent_cancel_requested = False
        self._tasks = set()
        self._errors = []
        self._base_error = None
        self._on_completed_fut = None

    def __repr__(self):
        info = ['']
        if self._tasks:
            info.append(f'tasks={len(self._tasks)}')
        if self._errors:
            info.append(f'errors={len(self._errors)}')
        if self._aborting:
            info.append('cancelling')
        elif self._entered:
            info.append('entered')

        info_str = ' '.join(info)
        return f'<TaskGroup{info_str}>'

    async def __aenter__(self):
        if self._entered:
            raise RuntimeError(
                f"TaskGroup {self!r} has already been entered")
        if self._loop is None:
            self._loop = events.get_running_loop()
        self._parent_task = tasks.current_task(self._loop)
        if self._parent_task is None:
            raise RuntimeError(
                f'TaskGroup {self!r} cannot determine the parent task')
        self._entered = True

        return self

    async def __aexit__(self, et: "Type[BaseException]", exc: BaseException, tb: TracebackType):
        self._exiting = True

        if (exc is not None and
                self._is_base_error(exc) and
                self._base_error is None):
            self._base_error = exc

        propagate_cancellation_error = \
            exc if et is exceptions.CancelledError else None
        if self._parent_cancel_requested:
            # If this flag is set we *must* call uncancel().
            if self._parent_task.uncancel() == 0:
                # If there are no pending cancellations left,
                # don't propagate CancelledError.
                propagate_cancellation_error = None

        if et is not None:
            if not self._aborting:
                # Our parent task is being cancelled:
                #
                #    async with TaskGroup() as g:
                #        g.create_task(...)
                #        await ...  # <- CancelledError
                #
                # or there's an exception in "async with":
                #
                #    async with TaskGroup() as g:
                #        g.create_task(...)
                #        1 / 0
                #
                self._abort()

        # We use while-loop here because "self._on_completed_fut"
        # can be cancelled multiple times if our parent task
        # is being cancelled repeatedly (or even once, when
        # our own cancellation is already in progress)
        while self._tasks:
            if self._on_completed_fut is None:
                self._on_completed_fut = self._loop.create_future()

            try:
                await self._on_completed_fut
            except exceptions.CancelledError as ex:
                if not self._aborting:
                    # Our parent task is being cancelled:
                    #
                    #    async def wrapper():
                    #        async with TaskGroup() as g:
                    #            g.create_task(foo)
                    #
                    # "wrapper" is being cancelled while "foo" is
                    # still running.
                    propagate_cancellation_error = ex
                    self._abort()

            self._on_completed_fut = None

        assert not self._tasks

        if self._base_error is not None:
            raise self._base_error

        # Propagate CancelledError if there is one, except if there
        # are other errors -- those have priority.
        if propagate_cancellation_error and not self._errors:
            raise propagate_cancellation_error

        if et is not None and et is not exceptions.CancelledError:
            self._errors.append(exc)


        if self._errors:
            # Exceptions are heavy objects that can have object
            # cycles (bad for GC); let's not keep a reference to
            # a bunch of them.
            try:
                import traceback
                import sys
                me = Exception('unhandled errors in a TaskGroup', self._errors)
                for e in self._errors:
                    traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
                raise me from None
            finally:
                self._errors = None

    def create_task(self, coro, *, name=None, context=None):
        """Create a new task in this group and return it.

        Similar to `asyncio.create_task`.
        """
        if not self._entered:
            raise RuntimeError(f"TaskGroup {self!r} has not been entered")
        if self._exiting and not self._tasks:
            raise RuntimeError(f"TaskGroup {self!r} is finished")
        if self._aborting:
            raise RuntimeError(f"TaskGroup {self!r} is shutting down")
        if context is None:
            task = self._loop.create_task(coro)
        else:
            task = self._loop.create_task(coro, context=context)
        _set_task_name(task, name)
        task.add_done_callback(self._on_task_done)
        self._tasks.add(task)
        return task

    # Since Python 3.8 Tasks propagate all exceptions correctly,
    # except for KeyboardInterrupt and SystemExit which are
    # still considered special.

    def _is_base_error(self, exc: BaseException) -> bool:
        assert isinstance(exc, BaseException)
        return isinstance(exc, (SystemExit, KeyboardInterrupt))

    def _abort(self):
        self._aborting = True

        for t in self._tasks:
            if not t.done():
                t.cancel()

    def _on_task_done(self, task: asyncio.Task):
        self._tasks.discard(task)

        if self._on_completed_fut is not None and not self._tasks:
            if not self._on_completed_fut.done():
                self._on_completed_fut.set_result(True)

        if task.cancelled():
            return

        exc = task.exception()
        if exc is None:
            return

        self._errors.append(exc)
        if self._is_base_error(exc) and self._base_error is None:
            self._base_error = exc

        if self._parent_task.done():
            # Not sure if this case is possible, but we want to handle
            # it anyways.
            self._loop.call_exception_handler({
                'message': f'Task {task!r} has errored out but its parent '
                           f'task {self._parent_task} is already completed',
                'exception': exc,
                'task': task,
            })
            print(f"Task {task!r} has errored out but its parent "
                  f'task {self._parent_task} is already completed'
                  f"Traceback (most recent call last):"
                    f"{exc.__traceback__}")
            return

        if not self._aborting and not self._parent_cancel_requested:
            # If parent task *is not* being cancelled, it means that we want
            # to manually cancel it to abort whatever is being run right now
            # in the TaskGroup.  But we want to mark parent task as
            # "not cancelled" later in __aexit__.  Example situation that
            # we need to handle:
            #
            #    async def foo():
            #        try:
            #            async with TaskGroup() as g:
            #                g.create_task(crash_soon())
            #                await something  # <- this needs to be canceled
            #                                 #    by the TaskGroup, e.g.
            #                                 #    foo() needs to be cancelled
            #        except Exception:
            #            # Ignore any exceptions raised in the TaskGroup
            #            pass
            #        await something_else     # this line has to be called
            #                                 # after TaskGroup is finished.
            self._abort()
            self._parent_cancel_requested = True
            self._parent_task.cancel()

def get_process_executor() -> "ProcessPoolExecutor":
    """Get an optimized ProcessPoolExecutor."""
    import atexit
    import os
    import signal
    if TYPE_CHECKING:
        import multiprocessing as mp
        import os
        import sys
        from concurrent.futures import ProcessPoolExecutor
        

    else:
        ProcessPoolExecutor = smart_import('concurrent.futures.ProcessPoolExecutor')
        mp = smart_import('multiprocessing')
        ctx = mp.get_context('fork')
        os = smart_import('os')
        signal = smart_import('signal')
        atexit = smart_import('atexit')
        T = TypeVar("T")


    ctx = mp.get_context('fork')
    # Calculate optimal workers based on CPU cores and task type
    cpu_count = os.cpu_count() or 1
    max_workers = min(cpu_count * 2, 32) # Double CPU count but cap at 32

    executor = ProcessPoolExecutor(
        max_workers=max_workers,
        mp_context=ctx,
        initializer=_process_initializer,
    )

    def _cleanup():
        executor.shutdown(wait=False, cancel_futures=True)
    atexit.register(_cleanup)

    # Improved signal handling
    def _signal_handler(signum, frame):
        executor.shutdown(wait=False, cancel_futures=True)
        sys.exit(128 + signum)

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    return executor

def _process_initializer():
    """Initialize process worker."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)

async def process_tasks(tasks: "Iterable[Awaitable[T]]") -> "AsyncIterator[T]":
    """Process tasks and yield as they complete.
    
    Example:
        Process multiple async tasks concurrently with error handling:

        ```python
        async def example():
            # Create some example tasks
            async def task1():
                await asyncio.sleep(1)
                return "Task 1 done"
                
            async def task2():
                await asyncio.sleep(2) 
                raise ValueError("Task 2 failed")
                
            async def task3():
                await asyncio.sleep(3)
                return "Task 3 done"

            # Process tasks
            tasks = [task1(), task2(), task3()]
            async for result in process_tasks(tasks):
                print(f"Got result: {result}")
                
            # Output:
            # Got result: Task 1 done
            # Task failed: Task 2 failed 
            # Got result: Task 3 done
        ```
    
    Args:
        tasks: An iterable of awaitable tasks to process concurrently

    Yields:
        Results from completed tasks, skipping failed ones

    Raises:
        asyncio.CancelledError: If processing is cancelled
    """

    async def worker(task: Awaitable[T]) -> T | None:
        try:
            return await asyncio.shield(task)
        except asyncio.CancelledError:
            return None
        except Exception as e:
            logging.error(f"Task failed: {e}")
            return None

    pending = {asyncio.create_task(worker(task)) for task in tasks}

    while pending:
        done, pending = await asyncio.wait(
            pending,
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in done:
            try:
                result = await task
                if result is not None:
                    yield result
            except Exception as e:
                console.print(f"Task failed: {e}", style="bold red")
                logging.error(f"Failed to process result: {e}")

class AsCompleted(Executor):
    def __init__(self, *tasks: Awaitable[Any]):
        super().__init__()
        self._shutdown = False
        self._shutdown_lock = RLock()
        self._futures: set[Future] = set()
        self._pending: set[Future] = set()
        self._initial_tasks = process_tasks(tasks)


    def submit(self, fn, *args, **kwargs) -> Future[Any]:
        print(f"{self=}, {fn=}, {args=}, {kwargs=}")
        if not isinstance(self, AsCompleted):
            if not args:
                args = ({},)
            kwargs = {**kwargs, **args[-1]}
            args = (fn,) + args[:-1]
            fn = asyncio.coroutine(self)
            self = AsCompleted()

        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            future: Future = asyncio.ensure_future(fn(*args, **kwargs))
            self._futures.add(future)
            self._pending.add(future)
            future.add_done_callback(self._on_future_done)
            return future

    def _on_future_done(self, future):
        self._pending.remove(future)

    def shutdown(self, wait=True):
        with self._shutdown_lock:
            self._shutdown = True
        if wait:
            for future in self._futures:
                future.result()

    def __aiter__(self):
        return self._initial_tasks

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        if timeout is not None:
            raise ValueError('timeout is not supported')
        futures = [self.submit(fn, *args) for args in zip(*iterables)]
        for future in futures:
            if future in self._pending:
                future.result()
        return [future.result() for future in futures]

    def __del__(self):
        self.shutdown(wait=False)

@overload
def get_executor(kind: 'Literal["process"]')-> "ProcessPoolExecutor":...
@overload
def get_executor(kind: 'Literal["thread"]')-> "ThreadPoolExecutor":...
@overload
def get_executor(kind: 'Literal["as_completed"]') -> "Iterable[Coroutine[Any, Any, Any]]":...
@lru_cache(None)
def get_executor(kind: 'Literal["process", "thread", "as_completed"]') -> "ThreadPoolExecutor | ProcessPoolExecutor | AsCompleted":
    """Get cached executor instance."""


    if kind == "thread":
        return ThreadPoolExecutor(
            max_workers=min(12, (os.cpu_count() or 1) * 4),
        )
    if kind == "process":
        return get_process_executor()
    if kind == "as_completed":
        return AsCompleted()
    raise ValueError(f"Invalid executor kind: {kind}")

async def main():
    async def worker(func: Callable[[], Any]) -> Any:
        print(f"{func()=}")
    
    exec = process_tasks([worker(lambda: 1), worker(lambda: 2)])
    async for result in exec:
        print(f"{result=}")

if __name__ == "__main__":
    asyncio.run(main())