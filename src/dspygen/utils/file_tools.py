import json
import tiktoken
import anyio
import yaml

from pathlib import Path


def extract_code(text: str) -> str:
    # Use a regular expression to find code blocks enclosed in triple backticks.
    text_code = re.findall(r"```([\s\S]+?)```", text)

    if not text_code:
        return text

    # Concatenate all the code blocks together with double newline separators.
    concatenated_code = "\n\n".join(
        [code[code.index("\n") + 1 :] for code in text_code]
    )

    return concatenated_code


import re


def slugify(text):
    # Convert the text to lowercase
    text = text.lower()

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


def project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent


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


def templates_dir(file_name="") -> Path:
    return source_dir() / "templates" / file_name


def pages_dir(file_name="") -> Path:
    return source_dir() / "pages" / file_name


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


# Test the function
def main():
    print(count_tokens(get_source(__file__)))


if __name__ == "__main__":
    main()
