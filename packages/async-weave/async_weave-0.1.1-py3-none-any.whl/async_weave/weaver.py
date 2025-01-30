import asyncio
import contextlib
import logging
import time
import uuid
from asyncio import Event, Queue, Task
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Generic,
    Optional,
    TypeVar,
    cast,
)

log = logging.getLogger(__name__)

T = TypeVar("T")  # Type for task result
ID = TypeVar("ID")  # Type for task ID


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskInfo(Generic[T]):
    status: TaskStatus
    attempts: int = 0
    last_attempt: float = 0
    error: Optional[Exception] = None
    result: Optional[T] = None
    on_complete: Optional[Callable[[Any, T], None]] = None
    on_error: Optional[Callable[[Any, Exception], None]] = None
    on_cancel: Optional[Callable[[Any], None]] = None

class AsyncWeaver(Generic[ID, T]):
    """
    Manages asynchronous task execution with retry capabilities and status monitoring.

    Generic Parameters:
        ID: Type of the task identifier
        T: Type of the task result
    """

    def __init__(
        self,
        worker_count: int = 10,
        max_retries: int = 1,
        retry_delay: float = 300,
        monitor_interval: float = 60.0,
        id_generator: Optional[Callable[..., ID]] = None,
    ):
        """
        Initialize the AsyncManager.

        Args:
            worker_count: Number of worker tasks
            max_retries: Maximum number of retries on task failure
            retry_delay: Time to wait before retrying a failed task
            monitor_interval: Interval to monitor task statuses
        """
        self.started = False
        self.task_queue: Queue[ID] = Queue()
        self.task_status: Dict[ID, TaskInfo[T]] = {}
        self.task_data: Dict[ID, tuple[Callable[..., Awaitable[T]], tuple, dict]] = {}
        self.shutdown_event = Event()
        self.workers: list[Task] = []
        self.monitor_task: Optional[Task] = None
        self.worker_count = worker_count
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.monitor_interval = monitor_interval
        self.running_tasks: Dict[ID, Task] = {}
        self.id_generator = id_generator or (lambda: cast(ID, str(uuid.uuid4())))

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.shutdown()

    async def add_task(
        self,
        task_func: Callable[..., Awaitable[T]],
        *args,
        task_id: Optional[ID] = None,
        on_complete: Optional[Callable[[ID, T], None]] = None,
        on_error: Optional[Callable[[ID, Exception], None]] = None,
        on_cancel: Optional[Callable[[ID], None]] = None,
        **kwargs,
    ) -> ID:
        """
        Add a new task to the queue.

        Args:
            task_func: Async function to execute
            *args: Positional arguments for task_func
            task_id: Optional custom task ID. If not provided, one will be generated
            on_complete: Callback function called with the result when task completes
            on_error: Callback function called with the exception when task fails
            on_cancel: Callback function called when task is cancelled
            **kwargs: Keyword arguments for task_func

        Returns:
            The task ID (either provided or generated)
        """
        actual_task_id = task_id if task_id is not None else self.id_generator()

        if actual_task_id not in self.task_status:
            self.task_status[actual_task_id] = TaskInfo[T](
                status=TaskStatus.PENDING,
                on_complete=on_complete,
                on_error=on_error,
                on_cancel=on_cancel,
            )
            self.task_data[actual_task_id] = (task_func, args, kwargs)
            await self.task_queue.put(actual_task_id)
            log.debug(f"Task {actual_task_id} added to the queue.")

        return actual_task_id

    async def cancel_task(self, task_id: ID) -> None:
        """Cancel a specific task if it's running."""
        if task_id in self.running_tasks:
            task = self.running_tasks[task_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            finally:
                if self.task_status[task_id].status != TaskStatus.CANCELLED:
                    self.task_status[task_id].status = TaskStatus.CANCELLED
                    task_info = self.task_status.get(task_id)
                    if task_info and task_info.on_cancel:
                        try:
                            task_info.on_cancel(task_id)
                        except Exception as callback_error:
                            log.error(
                                f"Error in cancellation callback for task {task_id}: {callback_error}"
                            )
                self.running_tasks.pop(task_id, None)
                log.debug(f"Task {task_id} has been cancelled.")

    async def cancel_all_tasks(self, clear_queue: bool = True) -> None:
        """
        Cancel all tasks regardless of their current state.

        Args:
            clear_queue: If True, also clear pending tasks from the queue
        """
        all_task_ids = set(self.task_status.keys())
        running_cancellations = [
            self.cancel_task(task_id) for task_id in list(self.running_tasks.keys())
        ]
        if running_cancellations:
            await asyncio.gather(*running_cancellations)

        for task_id in all_task_ids:
            task_info = self.task_status[task_id]
            if task_info.status not in {TaskStatus.CANCELLED, TaskStatus.COMPLETED}:
                task_info.status = TaskStatus.CANCELLED
                if task_info.on_cancel:
                    try:
                        task_info.on_cancel(task_id)
                    except Exception as callback_error:
                        log.error(
                            f"Error in cancellation callback for task {task_id}: {callback_error}"
                        )

        if clear_queue:
            while not self.task_queue.empty():
                try:
                    self.task_queue.get_nowait()
                    self.task_queue.task_done()
                except asyncio.QueueEmpty:
                    break
            log.debug("All tasks cancelled and queue cleared.")

    async def get_task_result(self, task_id: ID, timeout: Optional[float] = None) -> T:
        """
        Wait for and return the result of a specific task.

        Args:
            task_id: ID of the task to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            The task result

        Raises:
            asyncio.TimeoutError: If timeout is reached
            KeyError: If task_id doesn't exist
            RuntimeError: If task failed or completed without a result
        """

        async def _wait() -> T:
            while True:
                if task_id not in self.task_status:
                    raise KeyError(f"Task {task_id} not found")

                task_info = self.task_status[task_id]
                if task_info.status == TaskStatus.COMPLETED:
                    if task_info.result is None:
                        raise RuntimeError(f"Task {task_id} completed but returned no result")
                    return task_info.result
                elif (
                    task_info.status == TaskStatus.FAILED and task_info.attempts >= self.max_retries
                ):
                    raise RuntimeError(f"Task {task_id} failed: {task_info.error}")

                await asyncio.sleep(0.1)

        if timeout is not None:
            return await asyncio.wait_for(_wait(), timeout)
        return await _wait()

    async def wait_for_completion(self, timeout: Optional[float] = None) -> None:
        """
        Wait for all currently queued and running tasks to complete.

        Args:
            timeout: Maximum time to wait in seconds. If None, wait indefinitely.

        Raises:
            asyncio.TimeoutError: If timeout is reached before all tasks complete
        """
        try:
            if timeout is not None:
                await asyncio.wait_for(self.task_queue.join(), timeout=timeout)
            else:
                await self.task_queue.join()
        except asyncio.TimeoutError:
            raise  # Re-raise the timeout error for the caller to handle

    async def _worker(self, worker_id: int) -> None:
        """Worker that processes tasks from the queue."""
        while not self.shutdown_event.is_set():
            try:
                task_id = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                task_info = self.task_status.get(task_id)
                task_func, args, kwargs = self.task_data.get(task_id, (None, (), {}))

                if not task_info or not task_func:
                    self.task_queue.task_done()
                    continue

                if task_info.status in {TaskStatus.PENDING, TaskStatus.FAILED}:
                    if task_info.status == TaskStatus.FAILED and (
                        time.time() - task_info.last_attempt < self.retry_delay
                        or task_info.attempts >= self.max_retries
                    ):
                        self.task_queue.task_done()
                        continue

                    task_info.status = TaskStatus.IN_PROGRESS
                    task_info.attempts += 1
                    task_info.last_attempt = time.time()

                    try:
                        task: Task = asyncio.create_task(
                            cast(Coroutine[Any, Any, T], task_func(*args, **kwargs))
                        )
                        self.running_tasks[task_id] = task

                        try:
                            result = await task
                            if task_id in self.task_status:
                                task_info.status = TaskStatus.COMPLETED
                                task_info.result = result
                                if task_info.on_complete:
                                    try:
                                        task_info.on_complete(task_id, result)
                                    except Exception as callback_error:
                                        log.error(
                                            f"Error in completion callback for task {task_id}: {callback_error}"
                                        )
                        except asyncio.CancelledError:
                            if task_id in self.task_status:
                                task_info.status = TaskStatus.CANCELLED
                                task_info.error = None
                                if task_info.on_cancel:
                                    try:
                                        task_info.on_cancel(task_id)
                                    except Exception as callback_error:
                                        log.error(
                                            f"Error in cancellation callback for task {task_id}: {callback_error}"
                                        )
                            raise
                        except Exception as e:
                            if task_id in self.task_status:
                                task_info.status = TaskStatus.FAILED
                                task_info.error = e
                                if task_info.on_error:
                                    try:
                                        task_info.on_error(task_id, e)
                                    except Exception as callback_error:
                                        log.error(
                                            f"Error in error callback for task {task_id}: {callback_error}"
                                        )
                        finally:
                            self.running_tasks.pop(task_id, None)
                            self.task_queue.task_done()
                    except Exception as e:
                        log.error(f"Error creating task {task_id}: {e}")
                        if task_id in self.task_status:
                            task_info.status = TaskStatus.FAILED
                            task_info.error = e
                            if task_info.on_error:
                                try:
                                    task_info.on_error(task_id, e)
                                except Exception as callback_error:
                                    log.error(
                                        f"Error in error callback for task {task_id}: {callback_error}"
                                    )
                        self.task_queue.task_done()

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                log.error(f"Worker {worker_id} error: {e}")

    async def _monitor(self) -> None:
        """Monitor task statuses and requeue failed tasks if eligible."""
        while not self.shutdown_event.is_set():
            try:
                await asyncio.sleep(self.monitor_interval)
                log.debug("\nTask Status Update:")
                status_counts = {status: 0 for status in TaskStatus}
                for task_info in self.task_status.values():
                    status_counts[task_info.status] += 1
                log.debug(f"Status counts: {status_counts}")

                for task_id, task_info in self.task_status.items():
                    if (
                        task_info.status == TaskStatus.FAILED
                        and task_info.attempts < self.max_retries
                        and (time.time() - task_info.last_attempt) >= self.retry_delay
                    ):
                        await self.task_queue.put(task_id)
            except Exception as e:
                log.error(f"Monitor error: {e}")

    async def start(self) -> None:
        """Start workers and monitor."""
        if self.started:  # Add this check
            return

        self.started = True
        for i in range(self.worker_count):
            worker_task = asyncio.create_task(self._worker(i))
            self.workers.append(worker_task)
        self.monitor_task = asyncio.create_task(self._monitor())
        log.debug("AsyncManager started.")

    async def shutdown(self, timeout: Optional[float] = None, cancel_running: bool = True) -> None:
        """
        Gracefully shut down workers and monitor.

        Args:
            timeout: Maximum time to wait for tasks to complete
            cancel_running: Whether to cancel running tasks after timeout or if no timeout provided
        """
        if timeout is not None:
            try:
                await asyncio.wait_for(self.task_queue.join(), timeout)
            except asyncio.TimeoutError:
                if cancel_running:
                    await self.cancel_all_tasks(clear_queue=True)
        elif cancel_running:
            await self.cancel_all_tasks(clear_queue=True)

        self.shutdown_event.set()

        if self.monitor_task and not self.monitor_task.done():
            self.monitor_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.monitor_task

        for worker in self.workers:
            worker.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await worker
        log.debug("AsyncManager shutdown complete.")
