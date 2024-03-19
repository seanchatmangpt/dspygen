import yaml
from dspygen.modules.dspygen_module import DGModule

def process_yaml_pipeline(yaml_file):
    with open(yaml_file, 'r') as f:
        config = yaml.safe_load(f)

    result = None

    dg_modules = []

    for module_def in config['modules']:
        module_class = globals()[f"{module_def['module']}DGModule"]  # Get the module class by name
        module_instance = module_class(**module_def.get('args', {}))

        dg_modules.append(module_instance)

    # Pipe the modules together because we need to do __or__ operations
    for i in range(len(dg_modules) - 1):
        dg_modules[i] | dg_modules[i + 1]

    return dg_modules[-1].output


def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    dsl_result = process_yaml_pipeline('pipeline.yaml')
    print(dsl_result)


if __name__ == '__main__':
    main()
