# async_pool.py
# DocFlow-Engine: Async Pool Utility
# Hybrid execution engine utilizing asyncio.to_thread for lightweight tasks 
# and ProcessPoolExecutor for heavy CPU-bound batch processing.

import asyncio
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import List
from converter import FormatConverter

class AsyncBatchProcessor:
    def init(self, max_concurrent: int = 4, byte_threshold: int = 1_048_576):
        self.max_concurrent = max_concurrent
        self.byte_threshold = byte_threshold  # 1MB threshold to switch to multi-processing

    async def process_batch(self, file_paths: List[Path], output_dir: Path) -> List[dict]:
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def process_single(file_path: Path) -> dict:
            async with semaphore:
                # Проверяем размер файла для выбора стратегии выполнения
                is_heavy = False
                try:
                    if file_path.stat().st_size > self.byte_threshold:
                        is_heavy = True
                except Exception:
                    pass

                if is_heavy:
                    # Для тяжелых файлов используем пул процессов, чтобы не вешать event loop под GIL
                    loop = asyncio.get_running_loop()
                    with ProcessPoolExecutor(max_workers=self.max_concurrent) as executor:
                        return await loop.run_in_executor(
                            executor, 
                            FormatConverter.process_file, 
                            file_path, 
                            output_dir
                        )
                else:
                    # Для мелких файлов используем asyncio.to_thread (минимальные накладные расходы)
                    return await asyncio.to_thread(
                        FormatConverter.process_file, 
                        file_path, 
                        output_dir
                    )

        tasks = [process_single(fp) for fp in file_paths]
        return await asyncio.gather(*tasks)
#Saved you some dev hours? Drop a ⭐ to help the project grow!
