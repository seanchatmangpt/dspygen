import importlib
import dspy

from dspygen.dsl.dsl_models import SignatureDSLModel, ModuleDSLModel, PipelineDSLModel, LanguageModelConfig
from dspygen.modules.dsl_module import DSLModule
from dspygen.typetemp.functional import render


def create_signature_from_model(signature_model: SignatureDSLModel) -> type:
    """Create a DSPy Signature class from a SignatureDSLModel instance."""
    class_dict = {"__doc__": signature_model.docstring, "__annotations__": {}}

    # Process input fields
    for input_field in signature_model.inputs:
        name = input_field.name
        desc = input_field.desc
        field_instance = dspy.InputField(desc=desc)
        class_dict[name] = field_instance
        class_dict["__annotations__"][name] = dspy.InputField

    # Process output fields
    for output_field in signature_model.outputs:
        name = output_field.name
        desc = output_field.desc
        prefix = output_field.prefix
        field_instance = dspy.OutputField(prefix=prefix, desc=desc)
        class_dict[name] = field_instance
        class_dict["__annotations__"][name] = dspy.OutputField

    # Dynamically create the Signature class
    signature_class = type(signature_model.name, (dspy.Signature,), class_dict)
    return signature_class


def create_module_from_model(module_model: ModuleDSLModel, global_signatures) -> dspy.Module:
    """Create a DSPy Module from a ModuleDSLModel instance."""
    signature = global_signatures[module_model.signature]
    predictor = module_model.predictor
    args = module_model.args

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


def load_signature_class(signature_class_name: str):
    """
    Dynamically loads a signature class by its fully qualified name.
    """
    module_name, class_name = signature_class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def load_dspy_module_class(dspy_module_class_name: str):
    """
    Dynamically loads a signature class by its fully qualified name.
    """
    module_name, class_name = dspy_module_class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def execute_pipeline(file_path):
    pipeline_inst = PipelineDSLModel.from_yaml(file_path)

    # Gather the signatures from the YAML
    global_signatures = {signature.name: create_signature_from_model(signature) for signature in pipeline_inst.signatures}

    context = {}  # Shared context for all steps

    if not pipeline_inst.models:
        pipeline_inst.models = [LanguageModelConfig(label="default", name="OpenAI", args={})]

    for step in pipeline_inst.steps:
        # Retrieve the module definition based on the step's module name
        module_def = next((m for m in pipeline_inst.modules if m.name == step.module), None)

        # Resolve Jinja2 templates in arguments against the context
        rendered_args = {arg: render(str(value), **context) for arg, value in step.args.items()}

        # If the module definition is not found, then load the module with load_dspy_module_class
        if not module_def:
            module_inst = load_dspy_module_class(step.module)(**rendered_args)        # Resolve Jinja2 templates in arguments against the context
        else:
            # Check if the signature class is already loaded, if not try to load the module
            # Assuming `pipeline_inst.signatures` contains fully qualified names or similar identifiers:
            if module_def and module_def.signature != "" and module_def.signature not in global_signatures:
                signature_class = load_signature_class(module_def.signature)
                global_signatures[module_def.signature] = signature_class

            if step.signature != "" and step.signature not in global_signatures:
                signature_class = load_signature_class(step.signature)
                global_signatures[module_def.signature] = signature_class

            # Dynamically create a new module instance for this step
            signature = global_signatures[module_def.signature]
            predictor = module_def.predictor

            # Note: Additional logic may be required to dynamically resolve args from rendered_args
            module_inst = DSLModule(signature=signature, predictor=predictor, context=context, **rendered_args)

        lm_label = step.model

        # Find the lm class within the dspy module. Need to import the class dynamically from the dspy module
        lm_config = next((m for m in pipeline_inst.models if m.label == lm_label), None)

        lm_class = getattr(dspy, lm_config.name)
        lm_inst = lm_class(**lm_config.args)

        with dspy.context(lm=lm_inst):
            module_output = module_inst.forward(**rendered_args)

        # Optionally, update the context with this module's output if needed
        # This assumes a convention for naming outputs in the context, e.g., using the module's name
        context[step.module] = module_output

    return context


def main():
    context = execute_pipeline('/Users/candacechatman/dev/dspygen/src/dspygen/dsl/blog_pipeline.yaml')
    print(context)


if __name__ == '__main__':
    main()
