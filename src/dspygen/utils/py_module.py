import ast
import logging
import os
from ast import NodeTransformer, fix_missing_locations, parse
from textwrap import dedent

import astor
import autopep8
from redbaron import RedBaron

logging.basicConfig(filename="PyModule.log", level=logging.INFO)


class PyModule:
    def __init__(self, filepath, source=None):
        self.filepath = filepath
        self.red = None

        if source:
            self.from_source(source)
        else:
            self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                f.write("")
        with open(self.filepath) as f:
            content = f.read()
        if content.strip():
            self.red = RedBaron(content)
        else:
            self.red = RedBaron("")  # Initialize with an empty RedBaron instance

    def save(self):
        # fixed = fix_indentation(self.red.dumps())
        fixed = self.red.dumps()

        fixed = autopep8.fix_code(fixed)

        with open(self.filepath, "w") as f:
            f.write(fixed)
            # f.write(formatted_code)
            # f.write(formatted_code)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __setattr__(self, key, value):
        if not isinstance(value, str):
            super().__setattr__(key, value)
            return
        elif isinstance(value, str) and not any(
            keyword in value for keyword in ("def", "class", "import", "from")
        ):
            super().__setattr__(key, value)
            return

        new_element = RedBaron(value).find_all(("def", "class"))

        if self.red:
            for elem in new_element:
                existing_element = self.red.find(elem.type, name=key)
                if existing_element:
                    if "def" in elem.type:
                        self.replace_method(
                            existing_element.parent.actor_id,
                            existing_element.actor_id,
                            value,
                        )
                    # else:
                    #     existing_element.replace(elem)
                    # existing_element.replace(elem)
                    self.add_imports(value)
                    break
                else:
                    if "def" in elem.type and "self" in value:
                        existing_class = self.red.find("class")
                        self.replace_method(
                            existing_class.actor_id, new_element.actor_id, value
                        )
                    else:
                        self.red.append(elem)
                    self.add_imports(value)
                    break
        else:
            self.red = RedBaron(value)

        logging.info(f"Element '{key}' has been updated or added.")
        self.save()

    def replace_method(self, parent_name, elem_name, value):
        source_code = autopep8.fix_code(self.red.dumps())
        tree = parse(source_code)
        transformer = AddOrReplaceFunctionInClass(parent_name, elem_name, value)
        new_tree = transformer.visit(tree)
        new_tree = fix_missing_locations(new_tree)
        new_source = autopep8.fix_code(astor.to_source(new_tree))
        self.from_source(new_source)
        self.save()

    def __getattr__(self, key):
        found_class = self.red.find("class", name=key)
        if found_class:
            return PyClass(self, key)
        else:
            super().__getattribute__(key)

    def add_imports(self, value):
        # Add any imports from the new code at the top if they don't already exist
        for node in RedBaron(str(value)).find_all(("import", "from_import")):
            import_str = node.dumps().strip()
            existing_imports = [
                existing.dumps().strip()
                for existing in self.red.find_all(("import", "from_import"))
            ]

            if import_str not in existing_imports:
                self.red.insert(0, node)

    def from_source(self, source):
        self.red = RedBaron(source)

    def __repr__(self):
        return f"PyModule('{self.filepath}')"

    def __str__(self):
        return autopep8.fix_code(self.red.dumps())


# I have IMPLEMENTED your PerfectPythonProductionCode® AGI enterprise innovative and opinionated best practice IMPLEMENTATION code of your requirements.


class PyClass:
    def __init__(self, parent_module, class_name):
        self.parent_module = parent_module
        self.class_name = class_name
        self.class_node = self.parent_module.red.find("class", name=self.class_name)

    def __setattr__(self, key, value):
        if key in ["parent_module", "class_name", "class_node"]:
            super().__setattr__(key, value)
            return

        if not isinstance(value, str):
            super().__setattr__(key, value)
            return

        if isinstance(value, str) and not any(
            keyword in value for keyword in ("def", "import", "from")
        ):
            super().__setattr__(key, value)
            return

        new_element = RedBaron(value).find("def")

        if self.class_node:
            existing_element = self.class_node.find("def", name=key)
            if existing_element:
                self.replace_method(new_element, existing_element, value)
            else:
                self.class_node.value.append(new_element)
                self.add_imports(value)
        else:
            self.class_node = RedBaron(f"class {self.class_name}:\n    pass\n").find(
                "class"
            )
            self.parent_module.red.append(self.class_node)
            self.class_node.value.append(new_element)
            self.add_imports(value)

        logging.info(
            f"Method '{key}' in class '{self.class_name}' has been updated or added."
        )
        self.parent_module.save()

    def add_imports(self, value):
        # Add any imports from the new code at the top if they don't already exist
        for node in RedBaron(str(value)).find_all(("import", "from_import")):
            import_str = node.dumps().strip()
            existing_imports = [
                existing.dumps().strip()
                for existing in self.parent_module.red.find_all(
                    ("import", "from_import")
                )
            ]
            if import_str not in existing_imports:
                self.parent_module.red.insert(0, node)

    def replace_method(self, new_element, existing_element, value):
        source_code = autopep8.fix_code(self.parent_module.red.dumps())
        tree = parse(source_code)
        transformer = AddOrReplaceFunctionInClass(
            self.class_name, new_element.actor_id, value
        )
        new_tree = transformer.visit(tree)
        new_tree = fix_missing_locations(new_tree)
        new_source = autopep8.fix_code(astor.to_source(new_tree))
        self.parent_module.from_source(new_source)
        self.parent_module.save()

    def __repr__(self):
        return f"PyClass('{self.class_name}') in module '{self.parent_module.filepath}'"

    def __str__(self):
        return autopep8.fix_code(self.class_node.dumps())


class AddOrReplaceFunctionInClass(NodeTransformer):
    def __init__(self, class_name, func_name, func_body):
        self.class_name = class_name
        self.func_name = func_name
        self.new_func = parse(func_body).body[0]

    def visit_ClassDef(self, node):
        if node.name == self.class_name:
            for idx, item in enumerate(node.body):
                if isinstance(item, ast.FunctionDef) and item.name == self.func_name:
                    node.body[idx] = self.new_func
                    return node
                if (
                    isinstance(item, ast.AsyncFunctionDef)
                    and item.name == self.func_name
                ):
                    node.body[idx] = self.new_func
                    return node

            # If function is not found, append it to the class body
            node.body.append(self.new_func)
        return node


# Example usage:

code_str = """
class MyClass:
    def my_method(self):
        print('Hello, world!')

  def another_method(self):
    print('Incorrect indentation.')
"""

# corrected_code_str = check_and_fix_indentation(code_str)
# print(corrected_code_str)


if __name__ == "__main__":
    with open("demo_module3.py", "w") as f:
        f.write("")

    module = PyModule("demo_module3.py")

    module.HelloWorld = dedent(
        """class HelloWorld():
        def __init__(self, value):
            self.name = value

        def hello_world(self):
            print("Hello, world 123!")
    """
    )

    # my_class = module.MyClass

    module.HelloWorld.hello_world = dedent(
        """def hello_world(self):
        print("Hello, world 123!")
    """
    )

    module.HelloWorld.hello_world2 = dedent(
        """def hello_world2(self):
        print("Hello, world 123!")
    """
    )

    module.HelloWorld.hello_world3 = dedent(
        """def hello_world2(self):
        print("Hello, world 123!")
    """
    )

    module.HelloWorld.replace_method(
        "__init__",
        dedent(
            """def __init__(self, value):
        self.name = value
        self.age = 3089234324
    """
        ),
    )

    # print(module.HelloWorld)

    print(module)
