import asyncio
import time
from typing import Any

import pytest

from async_weave.weaver import AsyncWeaver, TaskStatus


class MockTask:
    def __init__(
        self, should_fail: bool = False, fail_times: int = 0, delay: float = 0, value: Any = True
    ):
        self.should_fail = should_fail
        self.fail_times = fail_times
        self.attempts = 0
        self.delay = delay
        self.called = 0
        self.value = value or True

    async def __call__(self, *args, **kwargs):
        self.called += 1
        self.attempts += 1
        if self.delay:
            await asyncio.sleep(self.delay)
        if self.should_fail and self.attempts <= self.fail_times:
            raise ValueError(f"Task failed on attempt {self.attempts}")
        return self.value


@pytest.mark.asyncio
async def test_basic_task_execution():
    """Test successful execution of a simple task"""
    async with AsyncWeaver(worker_count=2, retry_delay=0.1, monitor_interval=0.1) as manager:
        mock_task = MockTask()

        task_id = await manager.add_task(mock_task)
        await asyncio.sleep(0.2)  # Wait for task to complete

        assert manager.task_status[task_id].status == TaskStatus.COMPLETED
        assert mock_task.called == 1


@pytest.mark.asyncio
async def test_multiple_tasks():
    """Test handling multiple tasks concurrently"""
    async with AsyncWeaver(worker_count=10) as manager:
        tasks = [MockTask(delay=0.1) for _ in range(10)]
        task_ids = []

        for task in tasks:
            task_id = await manager.add_task(task)
            task_ids.append(task_id)

        await asyncio.sleep(0.15)  # Wait for tasks to complete

        for i, task in enumerate(tasks):
            assert manager.task_status[task_ids[i]].status == TaskStatus.COMPLETED
            assert task.called == 1


@pytest.mark.asyncio
async def test_task_with_custom_id():
    """Test that custom task IDs work correctly"""
    async with AsyncWeaver(worker_count=2) as manager:
        mock_task = MockTask()
        custom_id = "custom_task_id"

        task_id = await manager.add_task(mock_task, task_id=custom_id)
        await asyncio.sleep(0.1)

        assert task_id == custom_id
        assert manager.task_status[custom_id].status == TaskStatus.COMPLETED
        assert mock_task.called == 1


@pytest.mark.asyncio
async def test_task_retry_on_failure():
    """Test that failed tasks are retried appropriately"""
    async with AsyncWeaver(
        worker_count=2,
        retry_delay=0.1,
        monitor_interval=0.1,
        max_retries=3,
    ) as manager:
        mock_task = MockTask(should_fail=True, fail_times=2)

        task_id = await manager.add_task(mock_task)
        await asyncio.sleep(0.5)  # Wait for retries

        task_info = manager.task_status[task_id]
        assert task_info.status == TaskStatus.COMPLETED
        assert mock_task.attempts == 3  # Failed twice, succeeded on third try
        assert task_info.attempts == 3


@pytest.mark.asyncio
async def test_max_retries_exceeded():
    """Test that tasks are not retried beyond max_retries"""
    async with AsyncWeaver(
        worker_count=2, max_retries=3, retry_delay=0.1, monitor_interval=0.1
    ) as manager:
        mock_task = MockTask(should_fail=True, fail_times=5)  # Will always fail

        task_id = await manager.add_task(mock_task)
        await asyncio.sleep(0.5)  # Wait for max retries

        task_info = manager.task_status[task_id]
        assert task_info.status == TaskStatus.FAILED
        assert task_info.attempts == manager.max_retries
        assert mock_task.attempts == manager.max_retries


@pytest.mark.asyncio
async def test_retry_delay():
    """Test that retry delay is respected"""
    async with AsyncWeaver(
        worker_count=2, retry_delay=0.2, monitor_interval=0.1, max_retries=3
    ) as manager:
        start_time = time.time()
        mock_task = MockTask(should_fail=True, fail_times=1)

        task_id = await manager.add_task(mock_task)
        await asyncio.sleep(0.5)  # Wait for completion

        task_info = manager.task_status[task_id]
        assert task_info.status == TaskStatus.COMPLETED
        assert time.time() - start_time >= manager.retry_delay


@pytest.mark.asyncio
async def test_duplicate_task_ids():
    """Test that duplicate task IDs are handled appropriately"""
    async with AsyncWeaver(worker_count=2, retry_delay=0.1, monitor_interval=0.1) as manager:
        mock_task1 = MockTask()
        mock_task2 = MockTask()
        custom_id = "same_id"

        await manager.add_task(mock_task1, task_id=custom_id)
        await asyncio.sleep(0.1)
        await manager.add_task(mock_task2, task_id=custom_id)
        await asyncio.sleep(0.2)

        assert mock_task1.called == 1
        assert mock_task2.called == 0


@pytest.mark.asyncio
async def test_custom_id_generator():
    """Test that custom ID generator works correctly"""
    counter = 0

    def custom_id_gen():
        nonlocal counter
        counter += 1
        return f"task_{counter}"

    async with AsyncWeaver(worker_count=2, id_generator=custom_id_gen) as manager:
        mock_task = MockTask()

        task_id1 = await manager.add_task(mock_task)
        task_id2 = await manager.add_task(mock_task)

        assert task_id1 == "task_1"
        assert task_id2 == "task_2"


@pytest.mark.asyncio
async def test_completion_callback():
    """Test that completion callback is executed when task succeeds"""
    async with AsyncWeaver(worker_count=2) as manager:
        mock_task = MockTask(value="success")
        callback_called = False
        callback_result = None

        def on_complete(task_id, result):
            nonlocal callback_called, callback_result
            callback_called = True
            callback_result = result

        task_id = await manager.add_task(mock_task, on_complete=on_complete)
        await asyncio.sleep(0.2)  # Wait for task to complete

        assert callback_called
        assert callback_result == "success"
        assert manager.task_status[task_id].status == TaskStatus.COMPLETED


@pytest.mark.asyncio
async def test_bulk_task_cancellation():
    """Test cancelling multiple running tasks during shutdown"""
    async with AsyncWeaver(worker_count=5, retry_delay=0.1, monitor_interval=0.1) as manager:
        long_tasks = [MockTask(delay=1.0) for _ in range(3)]
        task_ids = []

        for task in long_tasks:
            task_id = await manager.add_task(task)
            task_ids.append(task_id)

        # Give tasks time to start
        await asyncio.sleep(0.2)

        # Verify tasks are running
        assert all(task_id in manager.running_tasks for task_id in task_ids)
        assert all(
            manager.task_status[task_id].status == TaskStatus.IN_PROGRESS for task_id in task_ids
        )

        # Shutdown with cancellation
        await manager.shutdown(timeout=0.1, cancel_running=True)

        # Verify all tasks were cancelled
        assert all(
            manager.task_status[task_id].status == TaskStatus.CANCELLED for task_id in task_ids
        )
        assert not manager.running_tasks


@pytest.mark.asyncio
async def test_monitor_requeue_behavior():
    """Test that the monitor correctly requeues failed tasks"""
    async with AsyncWeaver(
        worker_count=2,
        retry_delay=0.1,
        monitor_interval=0.1,
        max_retries=3,
    ) as manager:
        mock_task = MockTask(should_fail=True, fail_times=1)

        task_id = await manager.add_task(mock_task)
        await asyncio.sleep(0.3)  # Wait for initial failure and requeue

        task_info = manager.task_status[task_id]
        assert task_info.status == TaskStatus.COMPLETED
        assert mock_task.attempts == 2


@pytest.mark.asyncio
async def test_graceful_shutdown_with_completion():
    """Test shutdown waiting for tasks to complete"""
    async with AsyncWeaver(worker_count=2, retry_delay=0.1, monitor_interval=0.1) as manager:
        tasks = [MockTask(delay=0.1) for _ in range(3)]
        task_ids = []

        for task in tasks:
            task_id = await manager.add_task(task)
            task_ids.append(task_id)

        # Wait for tasks to complete before shutdown
        await asyncio.sleep(0.3)
        await manager.task_queue.join()

        # Now shutdown
        await manager.shutdown()

        # Verify shutdown state
        assert manager.shutdown_event.is_set()
        assert manager.task_queue.empty()
        assert all(worker.done() for worker in manager.workers)
        assert manager.monitor_task and manager.monitor_task.done()


@pytest.mark.asyncio
async def test_immediate_shutdown():
    """Test immediate shutdown with pending tasks"""
    async with AsyncWeaver(worker_count=2, retry_delay=0.1, monitor_interval=0.1) as manager:
        long_tasks = [MockTask(delay=0.5) for _ in range(3)]
        task_ids = []

        for task in long_tasks:
            task_id = await manager.add_task(task)
            task_ids.append(task_id)

        # Immediate shutdown without waiting
        await manager.shutdown(cancel_running=False)

        # Verify shutdown state
        assert manager.shutdown_event.is_set()
        assert all(worker.done() for worker in manager.workers)
        assert manager.monitor_task and manager.monitor_task.done()

        # Tasks should still be in queue since they didn't complete
        assert not manager.task_queue.empty()
        assert manager.task_queue.qsize() == 3

        # Verify task statuses
        for task_id in task_ids:
            assert task_id in manager.task_status
            assert manager.task_status[task_id].status in {
                TaskStatus.PENDING,
                TaskStatus.IN_PROGRESS,
            }


@pytest.mark.asyncio
async def test_individual_task_cancellation():
    """Test cancelling a specific task"""
    async with AsyncWeaver(worker_count=2, retry_delay=0.1, monitor_interval=0.1) as manager:
        long_task = MockTask(delay=1.0)  # Task that runs for 1 second

        task_id = await manager.add_task(long_task)

        # Give task time to start
        await asyncio.sleep(0.2)

        # Cancel the specific task
        await manager.cancel_task(task_id)

        # Verify task status
        assert manager.task_status[task_id].status == TaskStatus.CANCELLED
        assert task_id not in manager.running_tasks

        # Verify task was interrupted before completion
        assert long_task.called == 1  # Task was started
        await asyncio.sleep(1.0)  # Wait full task duration
        assert manager.task_status[task_id].status == TaskStatus.CANCELLED  # Still cancelled


@pytest.mark.asyncio
async def test_cancellation_with_retry():
    """Test that cancelled tasks are not retried"""
    async with AsyncWeaver(
        worker_count=2, retry_delay=0.1, monitor_interval=0.1, max_retries=3
    ) as manager:
        task = MockTask(delay=0.5)  # Long enough to cancel

        task_id = await manager.add_task(task)

        # Give task time to start
        await asyncio.sleep(0.2)

        # Cancel the task
        await manager.cancel_task(task_id)

        # Wait for potential retry
        await asyncio.sleep(0.5)

        # Verify task remains cancelled and wasn't retried
        assert manager.task_status[task_id].status == TaskStatus.CANCELLED
        assert task.called == 1  # Task should only have been called once


@pytest.mark.asyncio
async def test_shutdown_without_cancellation():
    """Test shutdown behavior when cancel_running=False"""
    async with AsyncWeaver(worker_count=2, retry_delay=0.1, monitor_interval=0.1) as manager:
        tasks = [MockTask(delay=0.3) for _ in range(2)]  # Tasks that take 0.3s to complete

        for i, task in enumerate(tasks):
            await manager.add_task(task, task_id=f"task_{i}")

        # Give tasks time to start
        await asyncio.sleep(0.1)

        # Shutdown without cancellation, but with timeout longer than task duration
        await manager.shutdown(timeout=0.5, cancel_running=False)

        # Verify tasks completed normally
        assert all(task.called == 1 for task in tasks)  # All tasks ran
        assert all(
            manager.task_status[f"task_{i}"].status == TaskStatus.COMPLETED
            for i in range(len(tasks))
        )


@pytest.mark.asyncio
async def test_error_callback():
    """Test that error callback is executed when task fails"""
    async with AsyncWeaver(worker_count=2, max_retries=1) as manager:
        mock_task = MockTask(should_fail=True, fail_times=2)  # Will always fail
        callback_called = False
        callback_error = None

        def on_error(task_id: str, error):
            nonlocal callback_called, callback_error
            callback_called = True
            callback_error = error

        task_id = await manager.add_task(mock_task, on_error=on_error)
        await asyncio.sleep(0.3)  # Wait for task to fail and retry

        assert callback_called
        assert isinstance(callback_error, ValueError)
        assert str(callback_error).startswith("Task failed on attempt")
        assert manager.task_status[task_id].status == TaskStatus.FAILED


@pytest.mark.asyncio
async def test_cancel_callback():
    """Test that cancel callback is executed when task is cancelled"""
    async with AsyncWeaver(worker_count=2) as manager:
        mock_task = MockTask(delay=0.5)  # Long enough to cancel
        callback_called = False

        def on_cancel(task_id: str):
            nonlocal callback_called
            callback_called = True

        task_id = await manager.add_task(mock_task, on_cancel=on_cancel)
        await asyncio.sleep(0.1)  # Give task time to start
        await manager.cancel_task(task_id)
        await asyncio.sleep(0.1)  # Wait for cancellation to process

        assert callback_called
        assert manager.task_status[task_id].status == TaskStatus.CANCELLED


@pytest.mark.asyncio
async def test_callback_error_handling():
    """Test that errors in callbacks don't affect task status"""
    async with AsyncWeaver(worker_count=2) as manager:
        mock_task = MockTask()

        def failing_callback(task_id: str, _):
            raise ValueError("Callback error")

        task_id = await manager.add_task(mock_task, on_complete=failing_callback)
        await asyncio.sleep(0.2)  # Wait for task to complete

        # Task should complete successfully despite callback error
        assert manager.task_status[task_id].status == TaskStatus.COMPLETED


@pytest.mark.asyncio
async def test_multiple_callbacks():
    """Test that all types of callbacks can be registered and executed"""
    async with AsyncWeaver(worker_count=2) as manager:
        mock_task = MockTask(delay=0.2)
        callbacks_called = {"complete": False, "error": False, "cancel": False}

        def on_complete(task_id: str, _):
            callbacks_called["complete"] = True

        def on_error(task_id: str, _):
            callbacks_called["error"] = True

        def on_cancel(task_id: str):
            callbacks_called["cancel"] = True

        task_id = await manager.add_task(
            mock_task, on_complete=on_complete, on_error=on_error, on_cancel=on_cancel
        )
        await asyncio.sleep(0.1)  # Give task time to start
        await manager.cancel_task(task_id)
        await asyncio.sleep(0.2)  # Wait for cancellation to process

        assert not callbacks_called["complete"]  # Should not be called
        assert not callbacks_called["error"]  # Should not be called
        assert callbacks_called["cancel"]  # Should be called
        assert manager.task_status[task_id].status == TaskStatus.CANCELLED


@pytest.mark.asyncio
async def test_bulk_cancel_callbacks():
    """Test that cancel callbacks are executed during bulk cancellation"""
    async with AsyncWeaver(worker_count=2) as manager:
        callback_executions = {}  # Track which tasks triggered callbacks

        def create_cancel_callback(task_id: str):
            def on_cancel(task_id: str):
                callback_executions[task_id] = callback_executions.get(task_id, 0) + 1

            return on_cancel

        tasks = [MockTask(delay=0.5) for _ in range(3)]
        task_ids = []

        for task in tasks:
            task_id = await manager.add_task(task)
            task_ids.append(task_id)
            # Update the task's cancel callback with its ID
            manager.task_status[task_id].on_cancel = create_cancel_callback(task_id)

        await asyncio.sleep(0.1)  # Give tasks time to start
        await manager.cancel_all_tasks()
        await asyncio.sleep(0.2)  # Wait for cancellations to complete

        # Check each task was cancelled exactly once
        for task_id in task_ids:
            assert callback_executions.get(task_id, 0) == 1
            assert manager.task_status[task_id].status == TaskStatus.CANCELLED
            assert task_id not in manager.running_tasks

        # Total cancellations should equal number of tasks
        assert sum(callback_executions.values()) == len(tasks)


@pytest.mark.asyncio
async def test_task_status_transitions():
    """Test that task status transitions work correctly"""
    manager = AsyncWeaver(worker_count=2)
    try:
        task = MockTask(delay=0.1)

        # Add task before starting
        task_id = await manager.add_task(task)
        assert manager.task_status[task_id].status == TaskStatus.PENDING

        # Start manager and wait for completion
        await manager.start()
        result = await manager.get_task_result(task_id, timeout=2.0)

        assert result is True  # MockTask returns True by default
        assert manager.task_status[task_id].status == TaskStatus.COMPLETED
        assert task.called == 1
    finally:
        await manager.shutdown(cancel_running=True)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
