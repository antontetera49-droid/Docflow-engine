# main.py
"""
DocFlow-Engine: CLI Entrypoint
"""

import sys
from core.parser import DocumentParser

def main():
    print("=== DocFlow-Engine v1.0.0 ===")
    print("High-performance document processing pipeline initialized.")
    if len(sys.argv) > 1:
        target = sys.argv[1]
        parser = DocumentParser(target)
        print("Metadata:", parser.extract_metadata())
    else:
        print("Usage: python main.py <path_to_document>")

if __name__ == "__main__":
    main()
