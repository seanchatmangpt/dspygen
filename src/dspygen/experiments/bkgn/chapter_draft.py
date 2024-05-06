from dspygen.rm.code_retriever import CodeRetriever


def main():
    path = "/Users/sac/dev/dspygen/src/dspygen/books/socratic_tutor/src"
    gitignore = "/Users/sac/dev/dspygen/.gitignore"  # Optional

    code_retriever = CodeRetriever(path, gitignore)
    result = code_retriever.forward("*md")
    for file_content in result.passages:
        print(file_content)  # Here, you can instead write to a Markdown file or process further.

    # If I want one file containing all the code snippets
    # with open("code_snippets.md", "w") as f:
    #     for file_content in result.passages:
    #         f.write(file_content)


if __name__ == '__main__':
    main()
