import ast
import textwrap
from pathlib import Path

from dspygen.utils.file_tools import find_gitignore, parse_gitignore, is_ignored, is_binary


class PythonCodeRetriever:
    def __init__(self, include_signatures=True, include_docstrings=False, include_executable_code=False):
        self.include_signatures = include_signatures
        self.include_docstrings = include_docstrings
        self.include_executable_code = include_executable_code

    def forward(self, path):
        path = Path(path)
        content = []
        if path.is_file():
            self.process_file(path, content)
        else:
            for file_path in path.rglob("*.py"):
                self.process_file(file_path, content)
        return content

    def process_file(self, file_path, content):
        with file_path.open("r", encoding="utf-8") as f:
            file_content = f.read()
        processed_content = self.process_content(file_content)
        file_info = f"## File: {file_path.relative_to(Path(file_path).parent.parent)}\n\n```python\n"
        content.append(file_info + processed_content + "\n```\n\n")

    def process_content(self, source_code):
        tree = ast.parse(source_code)
        extractor = CodeExtractor(source_code, self.include_signatures, self.include_docstrings, self.include_executable_code)
        extractor.visit(tree)
        return extractor.filtered_code

class CodeExtractor(ast.NodeVisitor):
    def __init__(self, source_code, include_signatures, include_docstrings, include_executable_code):
        self.source_code = source_code
        self.include_signatures = include_signatures
        self.include_docstrings = include_docstrings
        self.include_executable_code = include_executable_code
        self.filtered_code = ""
        self._source_lines = source_code.splitlines(keepends=True)

    def visit_FunctionDef(self, node):
        if self.include_signatures:
            self._include_node_signature(node)
        if self.include_docstrings and ast.get_docstring(node):
            self._include_docstring(node)
        if self.include_executable_code:
            self._include_node_body(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.filtered_code += f'Class: {node.name}\n'
        for child_node in node.body:
            if isinstance(child_node, ast.AnnAssign):
                target = ast.unparse(child_node.target).strip()
                annotation = ast.unparse(child_node.annotation).strip()
                assignment_string = f"{target}: {annotation}"

                if child_node.value:  # Optional value inclusion
                    value = ast.unparse(child_node.value).strip()
                    assignment_string += f" = {value}"

                self.filtered_code += assignment_string + "\n"

        self.generic_visit(node)

    def _include_node_signature(self, node):
        start_line = node.lineno - 1
        end_line = start_line + 1
        signature = ''.join(self._source_lines[start_line:end_line])
        self.filtered_code += textwrap.dedent(signature).strip() + '\n'

    def _include_docstring(self, node):
        docstring = ast.get_docstring(node)
        if docstring:
            dedented_docstring = textwrap.dedent(f'"""{docstring}"""\n')
            self.filtered_code += dedented_docstring

    def _include_node_body(self, node):
        body_lines = []
        for body_item in node.body:
            start_line = body_item.lineno - 1
            end_line = body_item.end_lineno
            body_lines.extend(self._source_lines[start_line:end_line])

        dedented_body = textwrap.dedent(''.join(body_lines))
        self.filtered_code += dedented_body

if __name__ == '__main__':
    # Example usage
    retriever = PythonCodeRetriever(include_signatures=True, include_docstrings=True, include_executable_code=True)
    filtered_code = retriever.forward('python_code_retriever.py')
    print(filtered_code)
