
from dspygen.rm.code_retriever import CodeRetriever

def get_md_from_dir(directory):
    """Retrieves code snippets from a specified directory using CodeRetriever.

    Args:
        directory (str): The path to the directory.
    """
    return get_files_from_directory(directory, "*md")


def get_files_from_directory(directory, query, gitignore=None):
    """Retrieves code snippets from a specified directory using CodeRetriever.

    Args:
        directory (str): The path to the directory.
        gitignore (str, optional): The path to a .gitignore file. Defaults to None.
    """
    code_retriever = CodeRetriever(directory, gitignore)
    result = code_retriever.forward(query)
    return result.passages  # Return the list of file contents

def get_introduction(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/introduction' directory."""
    return get_md_from_dir('/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/introduction')
    

def get_appendices(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/appendices' directory."""
    return get_md_from_dir('/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/appendices')
    

def get_language_models(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/foundations/language-models' directory."""
    return get_md_from_dir('/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/foundations/language-models')
    

def get_testing(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/testing' directory."""
    return get_md_from_dir('/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/testing')
    

def get_architecture(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/architecture' directory."""
    return get_md_from_dir('/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/architecture')
    

def get_infrastructure(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/implementation/infrastructure' directory."""
    return get_md_from_dir('/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/implementation/infrastructure')
    

def get_best_practices(): 
    """Retrieves code snippets from the '/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/best-practices' directory."""
    return get_md_from_dir('/Users/candacechatman/dev/dspygen/src/dspygen/books/socratic_tutor/src/best-practices')


def main():
    """Main function"""
    print(get_introduction())


if __name__ == '__main__':
    main()
