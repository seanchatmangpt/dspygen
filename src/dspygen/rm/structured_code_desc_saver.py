from pathlib import Path
from loguru import logger

# A mapping of code languages to file extensions
LANGUAGE_EXTENSIONS = {
    'python': 'py',
    'javascript': 'js',
    'java': 'java',
    'csharp': 'cs',
    'cpp': 'cpp',
    'html': 'html',
    'css': 'css',
    'ruby': 'rb',
    'go': 'go',
    'php': 'php',
    'shell': 'sh',
    'sql': 'sql',
}

def detect_language_and_extension(code: str) -> str:
    """Detect the programming language and return the appropriate file extensions."""
    if "```python" in code or code.strip().startswith(("import", "def", "class")):
        return LANGUAGE_EXTENSIONS['python']
    elif "```javascript" in code or code.strip().startswith(("function", "var", "let", "const")):
        return LANGUAGE_EXTENSIONS['javascript']
    elif "```java" in code or code.strip().startswith("public class"):
        return LANGUAGE_EXTENSIONS['java']
    elif "```cpp" in code or code.strip().startswith("#include"):
        return LANGUAGE_EXTENSIONS['cpp']
    elif "```html" in code or code.strip().startswith(("<!DOCTYPE html>", "<html>")):
        return LANGUAGE_EXTENSIONS['html']
    elif "```css" in code or code.strip().startswith("body {") or code.strip().endswith("}"):
        return LANGUAGE_EXTENSIONS['css']
    elif "```go" in code or code.strip().startswith("package main"):
        return LANGUAGE_EXTENSIONS['go']
    elif "```php" in code or code.strip().startswith("<?php"):
        return LANGUAGE_EXTENSIONS['php']
    elif "```sql" in code or code.strip().startswith(("SELECT", "INSERT", "UPDATE", "DELETE")):
        return LANGUAGE_EXTENSIONS['sql']
    elif "```shell" in code or code.strip().startswith("#!/bin/bash"):
        return LANGUAGE_EXTENSIONS['shell']
    else:
        # Default to .py if no specific language is detected
        return 'py'

def save_code_snippet(temp_code_directory: Path, document_id: str, snippet: str, description: str):
    """Save code snippet to a file with appropriate extensions."""
    extension = detect_language_and_extension(snippet)
    file_path = temp_code_directory / f"{document_id}.{extension}"
    with file_path.open("w", encoding="utf-8") as file:
        logger.debug(f"Saving code description to {description}")
        logger.debug(f"Saving code snippet to {snippet}")
        file.write(f"# {description}\n{snippet}")
    logger.debug(f"Saved code snippet to {file_path}")
    return file_path
