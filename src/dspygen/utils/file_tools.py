import json
import tiktoken
import anyio
import yaml

from pathlib import Path
from fnmatch import fnmatch

import tempfile
from contextlib import contextmanager


def extract_code(text: str) -> str:
    # Use a regular expression to find code blocks enclosed in triple backticks.
    text_code = re.findall(r"```([\s\S]+?)```", text)

    if not text_code:
        return text

    # Concatenate all the code blocks together with double newline separators.
    concatenated_code = "\n\n".join(
        [code[code.index("\n") + 1:] for code in text_code]
    )

    return concatenated_code


import re


def slugify(text):
    # Convert the text to lowercase
    text = text.lower()

    text = text.replace(" ", "-")

    # Replace spaces with hyphens and remove other non-alphanumeric characters
    text = re.sub(r"[^a-z0-9-]", "", text)

    # Replace multiple consecutive hyphens with a single hyphen
    text = re.sub(r"[-]+", "-", text)

    # Remove leading and trailing hyphens
    text = text.strip("-")

    return text


def find_project_root(current_path: Path | str = Path(__file__)) -> Path:
    """
    Traverse up from the current path to find the project root marker.
    """
    if isinstance(current_path, str):
        current_path = Path(current_path)

    # Define the name of your project root marker
    marker = "pyproject.toml"
    # Start from the current file's directory
    current_dir = current_path.parent
    while current_dir != current_dir.parent:  # stop at the root of the filesystem
        if (current_dir / marker).exists():
            return current_dir
        current_dir = current_dir.parent
    raise FileNotFoundError(f"Project root marker '{marker}' not found.")


def project_dir() -> Path:
    return Path(__file__).parent.parent.parent.parent


def data_dir(filename="") -> Path:
    return project_dir() / "data" / filename


def source_dir(file_name="") -> Path:
    return Path(__file__).parent.parent / file_name


def subcommands_dir(file_name="") -> Path:
    return source_dir() / "subcommands" / file_name


def dspy_modules_dir(file_name="") -> Path:
    return source_dir() / "modules" / file_name


def signatures_dir(file_name="") -> Path:
    return source_dir() / "signatures" / file_name


def lm_dir(file_name="") -> Path:
    return source_dir() / "lm" / file_name


def rm_dir(file_name="") -> Path:
    return source_dir() / "rm" / file_name


def templates_dir(file_name="") -> Path:
    return source_dir() / "templates" / file_name


def pages_dir(file_name="") -> Path:
    return source_dir() / "pages" / file_name


def dsl_dir(file_name="") -> Path:
    return source_dir() / "dsl" / file_name


def get_source(filename):
    # Read the source code from the file
    with open(filename, 'r') as file:
        source_code = file.read().replace(" ", "")

    return source_code


def is_dspygen():
    return "dspygen" in get_source(__file__)


def count_tokens(text: str, model: str = "gpt-4") -> int:
    enc = tiktoken.encoding_for_model("gpt-4")
    return len(enc.encode(text))


async def read(filename, to_type=None):
    async with await anyio.open_file(filename, mode="r") as f:
        contents = await f.read()
    if to_type == "dict":
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            contents = yaml.safe_load(contents)
        elif filename.endswith(".json"):
            contents = json.loads(contents)
    return contents


async def write(
        contents=None,
        *,
        filename=None,
        mode="w+",
        extension="txt",
        time_stamp=False,
        path="",
):
    # if extension == "yaml" or extension == "yml":
    #     contents = yaml.dump(
    #         contents, default_style="", default_flow_style=False, width=1000
    #     )
    # elif extension == "json":
    #     contents = json.dumps(contents)

    async with await anyio.open_file(path + filename, mode=mode) as f:
        await f.write(contents)
    return filename


@contextmanager
def tmp_file(content, mode='w+', delete=True):
    """
    Creates a temp file with content, yielding its path.

    Args:
        content (str): Content to write to the file.
        mode (str): File mode ('w+' for text, 'wb+' for binary).
        delete (bool): Delete file on exit (default True).

    Yields:
        str: The path to the temporary file.
    """
    with tempfile.NamedTemporaryFile(mode=mode, delete=delete) as tmp:
        # Write the content based on the mode
        if 'b' in mode:
            # Ensure content is bytes if in binary mode
            if isinstance(content, str):
                content = content.encode()  # Convert to bytes
            tmp.write(content)
        else:
            # Ensure content is str if in text mode
            if isinstance(content, bytes):
                content = content.decode()  # Convert to str
            tmp.write(content)

        tmp.flush()  # Ensure content is written
        yield tmp.name  # Provide file path


# Test the function
def main():
    print(count_tokens(get_source(__file__)))





def parse_gitignore(gitignore_path):
    if not gitignore_path.exists():
        return set()

    with gitignore_path.open("r", encoding="utf-8") as file:
        patterns = set(line.strip() for line in file if line.strip() and not line.startswith("#"))
    patterns.add(".git")  # Always ignore .git directory
    return patterns


def is_ignored(file_path, ignore_patterns):
    relative_path = file_path.relative_to(file_path.parents[len(ignore_patterns) - 1])
    return any(match_gitignore_pattern(relative_path, pattern) for pattern in ignore_patterns)


def match_gitignore_pattern(relative_path, pattern):
    if pattern.startswith("/"):
        if fnmatch(str(relative_path), pattern[1:]) or fnmatch(str(relative_path.parent), pattern[1:]):
            return True
    else:
        if any(fnmatch(str(path), pattern) for path in [relative_path, *relative_path.parents]):
            return True
    return False


def is_binary(file_path):
    try:
        with open(file_path, "rb") as file:
            return b"\x00" in file.read(1024)
    except IOError:
        return False


def find_gitignore(start_path):
    """
    Walks up the directory tree from the start_path to find a .gitignore file.

    :param start_path: The starting directory path as a Path object or string.
    :return: The path to the first .gitignore file found, or None if not found.
    """
    current_path = Path(start_path).resolve()  # Ensure we have an absolute path
    for parent in [current_path, *current_path.parents]:
        gitignore_path = parent / ".gitignore"
        if gitignore_path.exists():
            return gitignore_path
    return None


if __name__ == "__main__":
    main()
