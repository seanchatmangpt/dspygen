import dspy
from pathlib import Path
from fnmatch import fnmatch

from dspygen.utils.dspy_tools import init_ol, init_dspy


class CodeRetriever(dspy.Retrieve):
    def __init__(self, path, gitignore=None):
        super().__init__()
        self.path = Path(path)
        self.gitignore = Path(gitignore) if gitignore else self.path / ".gitignore"
        self.gitignore_patterns = self.parse_gitignore(self.gitignore)
        self.gitignore_patterns.add(".git")

    def parse_gitignore(self, gitignore_path):
        if not gitignore_path.exists():
            return set()

        with gitignore_path.open("r", encoding="utf-8") as file:
            patterns = set(
                line.strip() for line in file if line.strip() and not line.startswith("#")
            )
        return patterns

    def forward(self, query=None):
        content = []
        file_dict = {}
        for file_path in self.path.rglob("*"):
            if (
                    file_path.is_file()
                    and not self.is_ignored(file_path)
                    and (not query or self.is_filtered(file_path, query))
                    and not self.is_binary(file_path)
            ):
                try:
                    print(file_path)
                    with file_path.open("r", encoding="utf-8") as f:
                        file_content = f.read()
                        file_dict[file_path] = file_content
                except UnicodeDecodeError:
                    continue

                file_info = self.extract_file_info(file_path)
                content.append(file_info + file_content + "\n```\n\n")

        return dspy.Prediction(passages=content, file_dict=file_dict)

    def is_ignored(self, file_path):
        relative_path = file_path.relative_to(self.path)
        return any(
            self.match_gitignore_pattern(relative_path, pattern)
            for pattern in self.gitignore_patterns
        )

    def is_filtered(self, file_path, query):
        return fnmatch(file_path.name, query)

    def is_binary(self, file_path):
        try:
            with open(file_path, "rb") as file:
                return b"\x00" in file.read(1024)
        except IOError:
            return False

    def extract_file_info(self, file_path):
        file_extension = file_path.suffix.lstrip('.')
        file_info = f"## File: {file_path}\n\n```{file_extension}\n"
        return file_info

    def match_gitignore_pattern(self, relative_path, pattern):
        if pattern.startswith("/"):
            if fnmatch(str(relative_path), pattern[1:]) or fnmatch(str(relative_path.parent), pattern[1:]):
                return True
        else:
            if any(fnmatch(str(path), pattern) for path in [relative_path, *relative_path.parents]):
                return True
        return False


def get_files_from_directory(directory, query, gitignore=None):
    """Retrieves code snippets from a specified directory using CodeRetriever."""
    code_retriever = CodeRetriever(directory, gitignore)
    result = code_retriever.forward(query)
    return result.passages  # Return the list of file contents


def main():
    init_ol(model="phi3", max_tokens=2000)
    #init_dspy(model="gpt-4o", max_tokens=3000)
    path = "/Users/sac/dev/nuxt-ai-chatbot/stores"
    gitignore = "/.gitignore"  # Optional

    code_retriever = CodeRetriever(path, gitignore)
    result = code_retriever.forward("*.py") # and only the code after ```python and ending with ``` ")
    print(result.passages)

    for file_content in result.passages:
        #from dspygen.dspy_modules.nuxt_module import nuxt_call
        print(file_content)
        #nuxt = nuxt_call(path=path, readme=file_content)
        #print(nuxt)
    # for file_content in result.passages:
    #     print(file_content)  # Here, you can instead write to a Markdown file or process further.

    # If I want one file containing all the code snippets
    # with open("code_snippets.md", "w") as f:
    #     for file_content in result.passages:
    #         f.write(file_content)


if __name__ == '__main__':
    main()
