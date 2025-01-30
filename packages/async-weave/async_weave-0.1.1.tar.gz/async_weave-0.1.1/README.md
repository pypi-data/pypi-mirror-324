# AsyncWeaver

AsyncWeaver is a Python library for managing asynchronous tasks with retry capabilities and status monitoring. It provides a way to queue, execute, and track multiple concurrent tasks while handling failures and retries automatically.

## Features

- Concurrent task execution with configurable number of workers
- Automatic task retries with customizable delay
- Task status monitoring
- Support for task cancellation (individual or bulk)
- Callback support for task completion, failure, and cancellation
- Custom task ID generation
- Type hints for better IDE support

## Installation

```bash
pip install async-weave
```

## Basic Usage

```python
import asyncio
from async_weave import AsyncWeaver

async def example():
    # Create a manager with 5 workers, max 3 retries, and 5 minute retry delay
    async with AsyncWeaver(worker_count=5, max_retries=3, retry_delay=300) as manager:
        # Define an async task
        async def my_task(param):
            # Your task logic here
            return f"Processed {param}"
        
        # Add tasks to the queue
        task_id = await manager.add_task(my_task, "data")
        
        # Wait for result
        result = await manager.get_task_result(task_id)
        print(f"Task completed with result: {result}")

# Run the example
asyncio.run(example())
```

## Advanced Features

### Custom Task IDs

```python
task_id = await manager.add_task(my_task, task_id="custom_id_123")
```

### Callbacks

By default the task_id is a str, but if you set a custom task_id or a custom task id generator it will be the type you specified.

```python
async def example_with_callbacks():
    async with AsyncWeaver() as manager:
        def on_complete(task_id: str, result):
            print(f"Task completed with: {result}")
            
        def on_error(task_id: str, error):
            print(f"Task failed with: {error}")
            
        def on_cancel(task_id: str):
            print("Task was cancelled")
            
        await manager.add_task(
            my_task,
            on_complete=on_complete,
            on_error=on_error,
            on_cancel=on_cancel
        )
```

### Task Cancellation

```python
# Cancel a specific task
await manager.cancel_task(task_id)

# Cancel all running tasks
await manager.cancel_all_tasks()
```

### Custom ID Generator

```python
def custom_id_generator():
    return f"task_{time.time()}"

manager = AsyncWeaver(id_generator=custom_id_generator)
```

## Configuration Options

- `worker_count`: Number of concurrent workers (default: 10)
- `max_retries`: Maximum number of retry attempts for failed tasks (default: 1)
- `retry_delay`: Time to wait before retrying failed tasks in seconds (default: 300)
- `monitor_interval`: Interval for monitoring task status in seconds (default: 60)
- `id_generator`: Custom function for generating task IDs

## Task States

Tasks can be in the following states:
- `PENDING`: Task is queued but not yet started
- `IN_PROGRESS`: Task is currently running
- `COMPLETED`: Task finished successfully
- `FAILED`: Task failed and exceeded retry attempts
- `CANCELLED`: Task was cancelled

## Waiting for Task Completion

To wait for all tasks to complete, use the `wait_for_completion` method:

```python
# Wait indefinitely for all tasks to complete
await manager.wait_for_completion()

# Wait with a timeout
await manager.wait_for_completion(timeout=60)  # Wait up to 60 seconds
```

For individual tasks, you can wait for specific results:

```python
# Wait for a specific task to complete
result = await manager.get_task_result(task_id, timeout=30)
```

Note: When shutting down with `shutdown()`, you can control whether to wait for completion:
```python
# Wait for completion during shutdown
await manager.shutdown(timeout=60, cancel_running=False)

# Cancel running tasks during shutdown
await manager.shutdown(cancel_running=True)

## Testing

The project includes a comprehensive test suite. To run the tests:

```bash
pytest tests/
```

## License

[Insert your license here]