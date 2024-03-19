import sys
import types
import inspect
from typing import Callable


def module_to_dict(module, include_docstring=True) -> dict:
    module_dict = {
        "module_name": module.__name__,
        "docstring": module.__doc__ if include_docstring else None,
        "functions": {},
        "classes": {}
    }

    for name, obj in module.__dict__.items():
        if name.startswith("__"):
            continue
        # Check if the object is a function and is defined in the module
        if isinstance(obj, types.FunctionType) and obj.__module__ == module.__name__:
            module_dict["functions"][name] = function_to_dict(obj)
        # Check if the object is a class and is defined in the module
        elif isinstance(obj, type) and obj.__module__ == module.__name__:
            class_dict = {
                "class_name": obj.__name__,
                "docstring": obj.__doc__,
                "methods": {}
            }
            # Iterate through class dictionary to find methods
            for cname, cobj in obj.__dict__.items():
                if isinstance(cobj, types.FunctionType) and inspect.getmodule(cobj) == module:
                    class_dict["methods"][cname] = function_to_dict(cobj)
            module_dict["classes"][name] = class_dict

    return module_dict


def function_to_dict(func: Callable) -> dict:
    output = {
        "function_name": func.__name__,
        "docstring": func.__doc__,
        "keyword_arguments": {k: str(v) for k, v in func.__annotations__.items()},
    }

    output["keyword_arguments"].pop("return", None)  # Remove 'return' annotation if exists

    return output
