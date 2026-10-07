# async_pool.py
# DocFlow-Engine: Async Pool Utility
# Multi-threaded / asynchronous batch execution engine with detailed reporting.

import asyncio
from pathlib import Path
from typing import List, Callable, Any
from converter import FormatConverter

class AsyncBatchProcessor:
    def init(self, max_concurrent: int = 4):
        self.max_concurrent = max_concurrent

    async def process_batch(self, file_paths: List[Path], output_dir: Path) -> List[dict]:
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def sem_task(file_path: Path):
            async with semaphore:
                return FormatConverter.process_file(file_path, output_dir)

        tasks = [sem_task(fp) for fp in file_paths]
        return await asyncio.gather(*tasks)
#Saved you some dev hours? Drop a ⭐ to help the project grow!
