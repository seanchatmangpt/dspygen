import os
from jinja2 import Template, FileSystemLoader, Environment

from dspygen.typetemp.environment.typed_environment import environment
from dspygen.typetemp.functional import render

# Jinja Templates
BASE_TEMPLATE = '''
from dspygen.rm.code_retriever import CodeRetriever

def get_files_from_directory(directory, gitignore=None):
    """Retrieves code snippets from a specified directory using CodeRetriever.

    Args:
        directory (str): The path to the directory.
        gitignore (str, optional): The path to a .gitignore file. Defaults to None.
    """
    code_retriever = CodeRetriever(directory, gitignore)
    result = code_retriever.forward("*md")
    return result.passages  # Return the list of file contents
'''

FUNCTION_TEMPLATE = '''

def get_{{ directory.split('/')[-1] | underscore }}(): 
    """Retrieves code snippets from the '{{ directory }}' directory."""
    return get_files_from_directory('{{ directory }}')
    
'''

def get_leaf_directories(base_path):
    """Finds all leaf directories within a base path."""
    leaf_dirs = []
    for dirpath, dirnames, filenames in os.walk(base_path):
        if not dirnames:  # A leaf directory has no subdirectories
            leaf_dirs.append(dirpath)
            print(dirpath, dirnames, filenames)
    return leaf_dirs

def generate_file_retrieval_functions(base_path, output_file):
    """Generates function definitions using Jinja templates and writes them to a file."""
    leaf_dirs = get_leaf_directories(base_path)

    with open(output_file, "w") as f:
        f.write(render(BASE_TEMPLATE))
        for directory in leaf_dirs:
            # Skip __pycache__ directories
            if "__pycache__" in directory:
                continue
            f.write(render(FUNCTION_TEMPLATE, directory=directory))

# Example usage

def main():
    """Main function"""
    target = "/Users/candacechatman/dev/soc/src/soc"
    generate_file_retrieval_functions(target, "get_soc_files.py")

if __name__ == '__main__':
    main()
