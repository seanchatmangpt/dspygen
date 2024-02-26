from dspygen.typetemp.template.render_mixin import RenderMixin


class TypedTemplate(RenderMixin):
    """Base class for creating templated classes. Uses the jinja2 templating engine
    to render templates. Allows for usage of macros and filters.
    """

    template_path: str = ""  # The path to the file
    source: str = ""  # The string template to be rendered
    to: str = ""  # The "to" property for rendering destination
    output: str = ""  # The rendered output

    def __init__(self, **kwargs):
        if kwargs.get("template_path"):
            # Read the template to the source string
            with open(kwargs.get("template_path")) as f:
                self.source = f.read()

        self.__dict__.update(kwargs)

    def __call__(self, use_native=False, **kwargs) -> str:
        # Use NativeEnvironment when use_native is True, else use default Environment
        return self._render(use_native, **kwargs)

    def render(self, use_native=False, **kwargs) -> str:
        return self._render(use_native, **kwargs)
