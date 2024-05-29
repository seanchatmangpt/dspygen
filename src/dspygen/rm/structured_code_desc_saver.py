import os
import re
from pathlib import Path

def get_file_extension(code: str) -> str:
    """Detect the code language and return the appropriate file extension."""
    if re.search(r'\b(def|class)\b', code) and re.search(r'\bimport\b', code):
        return '.py'
    elif re.search(r'\b#template\b', code):
        return '.vue'
    elif re.search(r'\b(function|var|let|const)\b', code):
        return '.js'
    elif re.search(r'\b#include\b', code):
        return '.cpp'
    elif re.search(r'\bpublic\b', code) and re.search(r'\bstatic\b', code):
        return '.java'
    elif re.search(r'\b<!DOCTYPE html>\b', code):
        return '.html'
    else:
        return '.md'  # Default to .txt if no language is detected

def save_code_snippets(temp_code_directory: Path, document_id: str, code: str, description: str):
    """Save the code snippet to a file with the appropriate extension and description."""
    file_extension = get_file_extension(code)
    file_path = temp_code_directory / f"{document_id}{file_extension}"
    
    if code and description:
        with file_path.open("w", encoding="utf-8") as file:
            file.write(f"# {description}\n{code}")

    return file_path
