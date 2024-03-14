import yaml
from dspygen.modules.dsl_module import DSLModule, DEFAULT_SIGNATURE, DEFAULT_PREDICTOR
from dspygen.utils.dspy_tools import init_dspy


def initialize_module_from_yaml(yaml_file_path):
    # Load YAML content
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    signature = config.get("signature", DEFAULT_SIGNATURE)
    predictor = config.get("predictor", DEFAULT_PREDICTOR)
    args = config.get("args", [])

    # Prepare forward_args if args are meant for the forward method
    # Assuming args is a list of dictionaries where each dict represents kwargs for a method call
    forward_args = {}
    if isinstance(args, list):
        for arg in args:
            forward_args.update(arg)
    elif isinstance(args, dict):
        forward_args = args
    else:
        raise ValueError("Unsupported argument format in YAML.")

    # Initialize the module with predictor, signature, and forward_args
    module_inst = DSLModule(predictor=predictor, signature=signature, **forward_args)
    return module_inst





# Example usage
if __name__ == "__main__":
    init_dspy()
    module_path = "hello_world_module.yaml"
    module = initialize_module_from_yaml(module_path)
    # Example forward call
    output = module.forward()
    print(output)
