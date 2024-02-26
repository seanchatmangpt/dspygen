import inspect
import os
import re
from dataclasses import is_dataclass

from dspygen.typetemp.environment.typed_environment import environment


class TypedInjector:
    """Class for handling injections into existing files.
    Allows specifying injection properties like target_file, before, after, at_line, prepend, append, skip_if.
    """

    source: str = None  # The string template to be rendered
    to: str = None  # Target file where the content will be injected
    before: str = None  # Regular expression/text to locate before which the inject line will appear
    after: str = None  # Regular expression/text to locate after which the inject line will appear
    at_line: int = None  # Line number at which the inject line will appear
    prepend: bool = False  # Add line to start of file
    append: bool = False  # Add line to end of file
    skip_if: str = None  # Regular expression/text. If exists, injection is skipped
    output: str = None

    def __init__(self):
        # Check if the class is a dataclass and raise an error if it isn't
        if not is_dataclass(self):
            raise TypeError("TypedInjector classes must be dataclasses.")

    def __post_init__(self):
        """After the instance is initialized, create the jinja2 environment and
        template from the provided string.
        """
        self.env = environment

    def inject(self):
        """Public method to handle the injection based on the specified properties."""
        # Render the source template
        self.output = self.env.from_string(self.source).render(**self._properties())

        if self.skip_if and self._skip_if_exists():
            return
        elif self.prepend:
            self._inject_prepend()
        elif self.append:
            self._inject_append()
        elif self.at_line is not None:
            self._inject_at_line()
        elif self.before is not None:
            self._inject_before()
        elif self.after is not None:
            self._inject_after()

    def _properties(self):
        # Get the instance variables (not including methods or dunder methods)
        properties = {
            name: getattr(self, name)
            for name, value in inspect.getmembers(self)
            if not name.startswith("__") and not callable(value)
        }

        return properties

    def _inject_prepend(self):
        """Private method to prepend the content at the beginning of the file."""
        # Read the existing content of the file
        with open(self.to) as file:
            content = file.read()

        # Add the rendered source at the beginning of the file
        content = self.output + os.linesep + content

        # Write the updated content back to the file
        with open(self.to, "w") as file:
            file.write(content)

    def _inject_append(self):
        """Private method to append the content at the end of the file."""
        # Read the existing content of the file
        with open(self.to) as file:
            content = file.read()

        # Add the rendered source at the end of the file
        content += os.linesep + self.output

        # Write the updated content back to the file
        with open(self.to, "w") as file:
            file.write(content)

    def _inject_at_line(self):
        """Private method to inject the content at the specified line number."""
        # Read the existing content of the file
        with open(self.to) as file:
            content_lines = file.readlines()

        # Find the line containing the pattern and insert the rendered source after it
        for index, line in enumerate(content_lines):
            if index + 1 == self.at_line:
                content_lines.insert(index, self.output + os.linesep)
                break

        # Write the updated content back to the file
        with open(self.to, "w") as file:
            file.writelines(content_lines)

    def _inject_before(self):
        """Private method to inject the content before the specified text or pattern."""
        # Read the existing content of the file
        with open(self.to) as file:
            content_lines = file.readlines()

        # Find the line containing the pattern and add the rendered source before it
        for index, line in enumerate(content_lines):
            if re.search(self.before, line):
                content_lines.insert(index, self.output + os.linesep)
                break

        # Write the updated content back to the file
        with open(self.to, "w") as file:
            file.writelines(content_lines)

    def _inject_after(self):
        """Private method to inject the content before the specified text or pattern."""
        # Read the existing content of the file
        with open(self.to) as file:
            content_lines = file.readlines()

        # Find the line containing the pattern and add the rendered source before it
        for index, line in enumerate(content_lines):
            if re.search(self.after, line):
                content_lines.insert(index + 1, self.output + os.linesep)
                break

        # Write the updated content back to the file
        with open(self.to, "w") as file:
            file.writelines(content_lines)

    def _skip_if_exists(self):
        """Private method to check if the skip_if pattern exists in the file."""
        with open(self.to) as file:
            content = file.read()
            return re.search(self.skip_if, content) is not None
