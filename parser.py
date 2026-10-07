# parser.py
# DocFlow-Engine: Parser Module
# Extracts structure, text, and metadata from documents with detailed error tracking.

from pathlib import Path
from typing import Dict, Any

class DocumentParser:
    def init(self, file_path: str):
        self.file_path = Path(file_path)

    def extract_metadata(self) -> Dict[str, Any]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        stat = self.file_path.stat()
        return {
            "filename": self.file_path.name,
            "extension": self.file_path.suffix.lower(),
            "size_bytes": stat.st_size,
            "status": "parsed_successfully"
        }

    def parse_content(self) -> str:
        with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
#Saved you some dev hours? Drop a ⭐ to help the project grow!
