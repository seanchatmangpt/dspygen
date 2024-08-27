import objc
import jinja2

# Load EventKit dynamically
objc.loadBundle("EventKit", bundle_path="/System/Library/Frameworks/EventKit.framework", module_globals=globals())
EKEvent = objc.lookUpClass('EKEvent')


def extract_eKEvent_info():
    attributes = dir(EKEvent)

    methods = []
    properties = []

    for attr in attributes:
        if attr.startswith('_'):
            continue

        attr_value = getattr(EKEvent, attr)

        if callable(attr_value):
            methods.append(attr)
        else:
            properties.append(attr)

    return methods, properties


wrapper_template = """
class {{ class_name }}Wrapper:
    def __init__(self):
        self._{{ class_name.lower() }} = {{ class_name }}.alloc().init()

    {% for prop in properties %}
    @property
    def {{ prop|snake_case }}(self):
        return self._{{ class_name.lower() }}.{{ prop }}

    @{{ prop|snake_case }}.setter
    def {{ prop|snake_case }}(self, value):
        self._{{ class_name.lower() }}.{{ prop }} = value
    {% endfor %}

    {% for method in methods %}
    def {{ method|snake_case }}(self, *args, **kwargs):
        return self._{{ class_name.lower() }}.{{ method }}(*args, **kwargs)
    {% endfor %}
"""

import jinja2
import re

def snake_case_filter(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

# Create Jinja environment
env = jinja2.Environment()
env.filters['snake_case'] = snake_case_filter

def generate_wrapper(class_name, methods, properties):
    template = env.from_string(wrapper_template)
    return template.render(class_name=class_name, methods=methods, properties=properties)

def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    # Extract the methods and properties
    methods, properties = extract_eKEvent_info()

    # Generate the wrapper code
    wrapper_code = generate_wrapper("EKEvent", methods, properties)

    # Print the generated code
    # print(wrapper_code, file="ekevent_store_wrapper.py")

    # Write the wrapper code to disk
    with open("ekevent_wrapper.py", "w") as f:
        f.write(wrapper_code)

    print("EKEvent wrapper code has been written to ekevent_wrapper.py")


if __name__ == '__main__':
    main()
