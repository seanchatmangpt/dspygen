from dspygen.llm_pipe.dsl_pipeline_executor import execute_pipeline
from dspygen.rm.code_retriever import CodeRetriever

from loguru import logger

README = """
Overview
The Black Ocean Business Ecosystem SaaS Platform is an all-in-one solution that enables businesses to collaborate, innovate, and grow. It provides a suite of tools and services designed to streamline business operations, enhance productivity, and drive growth.

Features
Collaborative Environment: Break down industry barriers and collaborate with other businesses seamlessly.
Advanced Analytics: Leverage powerful analytics tools to gain deep insights into your business operations.
AI and Machine Learning: Integrate AI and machine learning to provide predictive analytics and intelligent insights.
Mobile Accessibility: Access the platform on the go with mobile applications for iOS and Android.
Ecosystem Development: Utilize APIs and SDKs to develop custom add-ons and extensions.
Internationalization: Localize the platform for different regions and languages to reach a global audience.
Industry-Specific Solutions: Tailored solutions for different sectors such as finance, healthcare, and retail.
Daisy UI: For components
Pinia: For state management
FormKit: For forms
Nuxt: For SSR
Vue 3 Composition API: For logic
"""


def main():
    # from dspygen.utils.dspy_tools import init_dspy
    # init_dspy(model="gpt-4o", max_tokens=1000)
    # init_ol(model="llama3", max_tokens=1000)
    path = "/Users/sac/dev/bobe/"

    cr = CodeRetriever(path)

    result = cr.forward("*.vue")

    logger.info(f"Found {len(result.file_dict)} files.")

    for path, content in result.file_dict.items():
        # print(path, content)
        with open(path, "w") as f:
            context = execute_pipeline('/Users/sac/dev/dspygen/src/dspygen/experiments/nuxt_code_ret/nuxt_gen_v2.yaml',
                                       component_path=str(path),
                                       readme=README)
            logger.info(f"Context: {context}")
            code = context.nuxt_source
            print(code)
            f.write(code)
            # f.write(str(context.initial_csd))


if __name__ == "__main__":
    main()
