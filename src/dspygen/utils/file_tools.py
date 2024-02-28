from pathlib import Path

import json
from time import gmtime, strftime

import anyio
import yaml

from dspygen.utils.complete import acreate
from dspygen.utils.models import get_model


async def gen_extension(
    prompt,
    min_chars=20,
    max_chars=60,
    char_limit=300,
    time_stamp=False,
    **completion_kwargs,
) -> str:
    prompt = prompt[:char_limit]

    completion_prompt = (
        f"Generate a concise filename based on the text: '{prompt}'. "
        f"The filename should:\n"
        f"- Be in lowercase letters.\n"
        f"- Have at least {min_chars} characters.\n"
        f"- Have at most {max_chars} characters.\n"
        f"- Use underscores as separators.\n"
        "Suggested filename:"
    )

    filename = await acreate(
        model=get_model("3i"),
        prompt=completion_prompt,
        temperature=0,
        max_tokens=max_chars * 2,
        stop=["\n"],
    )

    return filename.split(".")[-1]


async def generate_filename(
    prompt,
    prefix="",
    suffix="",
    extension="txt",
    min_chars=20,
    max_chars=60,
    char_limit=300,
    time_stamp=False,
    **completion_kwargs,
) -> str:
    prompt = prompt[:char_limit]

    completion_prompt = (
        f"Generate a concise filename based on the text: '{prompt}'. "
        f"The filename should:\n"
        f"- Be in lowercase letters.\n"
        f"- Have at least {min_chars} characters.\n"
        f"- Have at most {max_chars} characters.\n"
        f"- Use underscores as separators.\n"
        f"- Exclude file extensions.\n"
        "Suggested filename:"
    )

    filename = await acreate(
        model=get_model("3i"),
        prompt=completion_prompt,
        temperature=0,
        max_tokens=max_chars * 2,
        stop=["\n"],
    )

    # Post-process the filename
    filename = re.sub(r"[^a-zA-Z0-9_]", "", filename)
    filename = filename[:max_chars]

    if prefix:
        filename = f"{prefix}_{filename}"

    if suffix:
        filename = f"{filename}_{suffix}"

    if time_stamp:
        filename = f"{filename}_{strftime('%Y-%m-%d_%H-%M-%S', gmtime())}"

    if extension:
        filename = f"{filename}.{extension}"

    return filename


def extract_filename(text: str, allowed_extensions=None) -> str:
    """Extracts a filename from a text, aligning with Pythonic practices as advocated
    by Luciano Ramalho in "Fluent Python". It can also filter the search based on a list of allowed extensions.

    Args:
        text (str): The text from which to extract the filename.
        allowed_extensions (List[str], optional): A list of allowed file extensions (without the dot). Defaults to None.

    Returns:
        str: The extracted filename.

    Raises:
        ValueError: If no filename with allowed extensions is found.
    """
    # Create the regex pattern based on allowed extensions
    if allowed_extensions is None:
        allowed_extensions = ["py"]

    if allowed_extensions:
        pattern = rf'\b\w+[-\w]*\.({"|".join(allowed_extensions)})\b'
    else:
        pattern = r"\b\w+[-\w]*(\.\w+)\b"

    match = re.search(pattern, text)

    if match:
        return match.group(0)
    else:
        raise ValueError("No filename with allowed extensions found.")


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

    if not filename:
        filename = await generate_filename(
            prompt=contents, extension=extension, time_stamp=time_stamp
        )
        print(f"Writing to {filename}")

    async with await anyio.open_file(path + filename, mode=mode) as f:
        await f.write(contents)
    return filename


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


def project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent


def source_dir() -> Path:
    return Path(__file__).parent.parent


def subcommands_dir() -> Path:
    return source_dir() / "subcommands"


def dspy_modules_dir() -> Path:
    return source_dir() / "modules"


def signatures_dir() -> Path:
    return source_dir() / "signatures"


def lm_dir() -> Path:
    return source_dir() / "lm"


def get_source(filename):
    # Read the source code from the file
    with open(filename, 'r') as file:
        source_code = file.read().replace(" ", "")

    return source_code

import tiktoken


def count_tokens(text: str, model: str = "gpt-4") -> int:
    enc = tiktoken.encoding_for_model("gpt-4")
    return len(enc.encode(text))

# Test the function
def main():
    print(count_tokens(get_current_module_source()))


if __name__ == "__main__":
    main()
