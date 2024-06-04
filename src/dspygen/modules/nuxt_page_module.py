"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy
import os
import subprocess


class NuxtPageModule(dspy.Module):
    """NuxtPageModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, requirements):
        pred = dspy.Predict("requirements -> nuxt_page_name")
        self.output = pred(requirements=requirements).nuxt_page_name
        return self.output


def nuxt_page_name_call(requirements):
    nuxt_page_name = NuxtPageModule()
    return nuxt_page_name.forward(requirements=requirements)


def main():
    init_dspy()
    requirements = "Todo List"
    result = nuxt_page_name_call(requirements=requirements)
    print(result)
    # Trigger the generation with the result as the name argument
    generate_nuxt_page(result)


def generate_nuxt_page(page_name):
    os.chdir(os.path.expanduser('~/dev/nuxtgen'))
    subprocess.run(['hygen', 'page', 'new', page_name])


if __name__ == "__main__":
    main()
