from dspygen.experiments.done.gen_pydantic_class import PydanticClassTemplateSpecificationModel, class_template_str
from dspygen.experiments.gherkin_gen.gherkin_models import Comment, DocString, DataTable, Step
from sungen.typetemp.template.render_funcs import render_file, render_str
from sungen.typetemp.template.render_mixin import RenderMixin
from textwrap import dedent

from sungen.utils.str_tools import pythonic_str


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_lm

    # init_dspy(lm_class=Groq, model="llama-3.2-90b-text-preview")
    # init_dspy(lm_class=Groq, model="llama-3.1-70b-versatile")
    # init_lm("groq/llama-3.1-8b-instant", model_type="chat", max_tokens=2000)
    init_lm("groq/llama-3.1-70b-versatile", model_type="chat", max_tokens=2000)

    from sungen.dspy_modules.gen_pydantic_instance import GenPydanticInstance
    instance = GenPydanticInstance(PydanticClassTemplateSpecificationModel)("Gherkin Syntax Class: Scenario")

    render_str(class_template_str, model=instance, dest=f"{pythonic_str(instance.class_name)}.py")

    # instance = GenPydanticInstance(DocString)("Create a docstring that describes a gherkin feature that prints Hello World and the content type is markdown.")
    # print(instance)



    # from sungen.utils.dspy_tools import predict_type
    # model_inst = predict_type({"instruction": "Create a docstring that describes a gherkin feature that prints Hello World and the content type is markdown."},
    #                           DocString)
    # docstring = render_file("docstring.j2", **model_inst.model_dump())
    # print(docstring)




if __name__ == '__main__':
    main()
