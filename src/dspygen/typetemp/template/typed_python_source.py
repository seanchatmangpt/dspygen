from _ast import stmt
from ast import parse
from dataclasses import dataclass
from typing import Optional

from dspygen.typetemp.environment.typed_environment import TypedEnvironment
from dspygen.typetemp.environment.typed_native_environment import TypedNativeEnvironment
from dspygen.typetemp.template.render_mixin import RenderMixin

_env = TypedEnvironment()
_native_env = TypedNativeEnvironment()


@dataclass
class TypedPythonSource(RenderMixin):
    """Base class for creating templated classes. Uses the jinja2 templating engine
    to render templates. Allows for usage of macros and filters.
    """

    source: str = None  # The string template to be rendered
    use_native: bool = False  # Whether to use NativeEnvironment for rendering
    to: str = None  # The "to" property for rendering destination
    output: str = None  # The rendered output

    def __post_init__(self):
        """After the instance is initialized, set the environment"""
        # Use NativeEnvironment when use_native is True, else use default Environment
        self.env = _native_env if self.use_native else _env

    def __call__(self, **kwargs) -> str:
        return self._render(**kwargs)

    def render_function(self, **kwargs) -> stmt:
        """Renders the function template and returns its AST object.

        :param kwargs: The keyword arguments to be used in rendering
        :return: The AST object of the rendered function
        """
        rendered_func = self._render(**kwargs)
        return parse(rendered_func).body[0]

    def render_class(self, func_tmpls: Optional[list[str]] = None, **kwargs):
        """Renders the class template and returns the compiled class, optionally including methods.

        :param func_tmpls: A list of template strings for functions to be included in the class
        :param kwargs: The keyword arguments to be used in rendering
        :return: The compiled class
        """
        # Render the class
        rendered_cls = self._render(**kwargs)
        class_ast = parse(rendered_cls)

        # If function templates are provided, render and add them to the class
        if func_tmpls:
            for func_tmpl in func_tmpls:
                function_ast = None  #  render_function(func_tmpl, **kwargs)
                class_ast.body[-1].body.append(function_ast)

        # Compile the class AST
        compiled_class_def = compile(class_ast, filename="<ast>", mode="exec")
        class_dict = {}
        exec(compiled_class_def, class_dict)

        # Return the compiled class
        return class_dict[kwargs["class_name"]]
