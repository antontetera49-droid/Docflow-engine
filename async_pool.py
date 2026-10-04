# async_pool.py
#DocFlow-Engine: Async Pool Utility
#Multi-threaded / asynchronous batch execution engine.

import asyncio
from typing import Callable, List, Any

class AsyncBatchProcessor:
    def init(self, max_concurrent: int = 4):
        self.max_concurrent = max_concurrent

    async def process_batch(self, items: List[Any], task_func: Callable) -> List[Any]:
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def sem_task(item):
            async with semaphore:
                if asyncio.iscoroutinefunction(task_func):
                    return await task_func(item)
                else:
                    return task_func(item)

        tasks = [sem_task(item) for item in items]
        return await asyncio.gather(*tasks)
