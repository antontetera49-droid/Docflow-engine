# converter.py
# DocFlow-Engine: Converter Module
# Handles high-speed format translation with explicit error boundaries.

import json
from pathlib import Path

class FormatConverter:
    SUPPORTED_EXTENSIONS = {".md", ".txt"}

    @staticmethod
    def convert_markdown_to_html(raw_text: str) -> str:
        lines = raw_text.splitlines()
        html_lines = []
        for line in lines:
            if line.startswith("# "):
                html_lines.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith("## "):
                html_lines.append(f"<h2>{line[3:]}</h2>")
            else:
                html_lines.append(f"<p>{line}</p>")
        return "\n".join(html_lines)

    @classmethod
    def process_file(cls, file_path: Path, output_dir: Path) -> dict:
        result_record = {
            "source_path": str(file_path),
            "output_path": None,
            "converter_version": "v1.0.0",
            "status": "failed",
            "error_reason": None
        }

        if file_path.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
            result_record["error_reason"] = f"Unsupported format: {file_path.suffix}"
            return result_record

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if file_path.suffix.lower() == ".md":
                converted = cls.convert_markdown_to_html(content)
                out_path = output_dir / f"{file_path.stem}.html"
            else:
                data = {
                    "length_chars": len(content),
                    "lines_count": len(content.splitlines()),
                    "content_preview": content[:200]
                }
                converted = json.dumps(data, indent=4)
                out_path = output_dir / f"{file_path.stem}.json"

            # Failure protection: write to temporary file, then rename atomically
            temp_out = out_path.with_suffix(out_path.suffix + ".tmp")
            temp_out.write_text(converted, encoding="utf-8")
            temp_out.replace(out_path)

            result_record["output_path"] = str(out_path)
            result_record["status"] = "success"
        except Exception as e:
            result_record["error_reason"] = str(e)

        return result_record
#Saved you some dev hours? Drop a ⭐ to help the project grow!
