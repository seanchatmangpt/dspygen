from jinja2 import FileSystemLoader
from jinja2.nativetypes import NativeEnvironment

from dspygen.typetemp.extension.faker_extension import FakerExtension
from dspygen.typetemp.extension.inflection_extension import InflectionExtension
from dspygen.utils.file_tools import templates_dir


class TypedNativeEnvironment(NativeEnvironment):
    def __init__(self, **kwargs):
        super(TypedNativeEnvironment, self).__init__(**kwargs)

        self.add_extension(FakerExtension)
        self.add_extension(InflectionExtension)
        self.add_extension("jinja2_time.TimeExtension")
        self.add_extension("jinja2.ext.i18n")
        self.add_extension("jinja2.ext.debug")
        self.add_extension("jinja2.ext.do")
        self.add_extension("jinja2.ext.loopcontrols")


file_loader = FileSystemLoader(templates_dir())

native_environment = TypedNativeEnvironment(loader=file_loader)

async_native_environment = TypedNativeEnvironment(enable_async=True, loader=file_loader)
