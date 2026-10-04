# converter.py
#DocFlow-Engine: Converter Module
#Handles high-speed format translation (Markdown <-> HTML <-> JSON).


import json

class FormatConverter:
    @staticmethod
    def md_to_html(md_text: str) -> str:
        lines = md_text.splitlines()
        html_lines = []
        for line in lines:
            if line.startswith("# "):
               N html_lines.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith("## "):
                html_lines.append(f"<h2>{line[3:]}</h2>")
            else:
                html_lines.append(f"<p>{line}</p>")
        return "\n".join(html_lines)

    @staticmethod
    def text_to_json(raw_text: str) -> str:
        data = {
            "length_chars": len(raw_text),
            "lines_count": len(raw_text.splitlines()),
            "content_preview": raw_text[:200]
        }
        return json.dumps(data, indent=4)
