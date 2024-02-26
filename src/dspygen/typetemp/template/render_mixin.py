import os
from typing import Any

from ..environment.typed_environment import environment
from ..environment.typed_native_environment import native_environment
from ..template.render_funcs import render_str


class RenderMixin:
    """A mixin class that encapsulates the render and _render_vars functionality.
    This class checks for the required properties 'source', 'env', 'to', and 'output'.
    """

    def _render(self, use_native=False, **kwargs) -> Any:
        """Render the template. Excludes instance variables that
        are not callable (i.e., methods) and don't start with "__".
        """
        env = native_environment if use_native else environment
        template = env.from_string(self.source)

        render_dict = {**self._render_vars(), **kwargs}

        self.output = template.render(**render_dict)

        # Render the "to" property if it's defined
        if self.to == "stdout":
            print(self.output)
        elif self.to:
            to_template = env.from_string(self.to)
            rendered_to = os.path.join(to_template.render(**render_dict))

            # Create the directory if it doesn't exist
            print(rendered_to)

            if not rendered_to.startswith(".") or not rendered_to.startswith("/"):
                rendered_to = "./" + str(rendered_to)

            os.makedirs(os.path.dirname(rendered_to), exist_ok=True)

            with open(rendered_to, "w") as file:
                file.write(self.output)

        return self.output

    def _render_vars(self) -> dict[str, Any]:
        """Get the instance variables (not including methods or dunder methods)."""
        # copy the self dict
        properties = self.__class__.__dict__.copy()
        properties.update(self.__dict__.copy())
        del properties["source"]

        # If the value of a property is a TypedTemplate, render it
        for name, value in properties.items():
            if isinstance(value, RenderMixin):
                properties[name] = value._render(**properties)
            elif isinstance(value, str):
                properties[name] = render_str(value, **properties)

        return properties
