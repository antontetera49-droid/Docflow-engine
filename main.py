# main.py
# DocFlow-Engine: CLI Entrypoint
import sys
import json
from pathlib import Path
from async_pool import AsyncBatchProcessor

async def amain():
    print("--- DocFlow-Engine v1.0.0 ---")
    print("High-performance resilient document processing pipeline initialized.")
    
    if len(sys.argv) > 2:
        input_dir = Path(sys.argv[1])
        output_dir = Path(sys.argv[2])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        files = [f for f in input_dir.iterdir() if f.is_file() and not f.name.endswith(".tmp")]
        print(f"Found {len(files)} files to process.")
        
        processor = AsyncBatchProcessor(max_concurrent=4)
        report = await processor.process_batch(files, output_dir)
        
        report_path = output_dir / "execution_report.json"
        report_path.write_text(json.dumps(report, indent=4), encoding="utf-8")
        print(f"Processing complete. Report saved to {report_path}")
    else:
        print("Usage: python main.py <input_dir> <output_dir>")

if __name__ == "__main__":
    asyncio.run(amain())
