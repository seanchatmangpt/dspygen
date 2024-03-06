from jinja2 import Environment, FileSystemLoader

from dspygen.typetemp.extension.faker_extension import FakerExtension
from dspygen.typetemp.extension.inflection_extension import InflectionExtension
from dspygen.utils.file_tools import templates_dir


class TypedEnvironment(Environment):
    def __init__(self, **kwargs):
        super(TypedEnvironment, self).__init__(
            trim_blocks=True, lstrip_blocks=True, **kwargs
        )

        self.add_extension(FakerExtension)
        self.add_extension(InflectionExtension)
        self.add_extension("jinja2_time.TimeExtension")
        self.add_extension("jinja2.ext.i18n")
        self.add_extension("jinja2.ext.debug")
        self.add_extension("jinja2.ext.do")
        self.add_extension("jinja2.ext.loopcontrols")

        self.filters["to_kwarg"] = lambda input_name: f"{input_name}={input_name}"


file_loader = FileSystemLoader(templates_dir())

environment = TypedEnvironment(loader=file_loader)

async_environment = TypedEnvironment(enable_async=True, loader=file_loader)
