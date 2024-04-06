from datetime import datetime
from random import choice

import anyio
import dspy
from asyncer import create_task_group

from dspygen.lm.groq_lm import Groq

from faker import Faker

from dspygen.rm.chatgpt_chromadb_retriever import ChatGPTChromaDBRetriever
from dspygen.typetemp.functional import render

dfss_black_belt_curriculum = [
    # Introduction
    "Introduction to Design for Lean Six Sigma",

    # Define Phase
    "Overview of the Define Phase",
    "Charter, MGPP, Risk Management, Communication Plan",

    # Measure Phase
    "Voice of the Customer",
    "Quality Function Deployment",
    "Target Costing",
    "Scorecards",
    "Intro to Minitab",
    "Basic Statistics",
    "Understanding Variation and Control Charts",
    "Measurement Systems Analysis",
    "Process Capability",

    # Explore Phase
    "Concept Generation",
    "TRIZ for New Product Design",
    "Transactional TRIZ",
    "Concept Selection – Pugh and AHP",
    "Statistical Tolerance Design",
    "Monte Carlo Simulation",
    "Hypothesis Testing",
    "Confidence Intervals",
    "Texting Means, Medians, and Variances",  # Assuming a typo, should be "Testing"
    "Proportion and Chi-Square",
    "Simple and Multiple Regression",
    "Multi-Vari Analysis",
    "Design FMEA",

    # Develop Phase
    "Detailed Design",
    "2-Way ANOVA",
    "Intro to Design of Experiments",
    "Full-Factorial DOE",
    "Fractional Factorial DOE",
    "DOE Catapult Simulation",
    "Key Lean Concepts",
    "Lean Design",
    "Design for Manufacture and Assembly",
    "Intro to Reliability",
    "Design of Experiments with Curvature",
    "Conjoint Analysis",
    "Mixture Designs",
    "Robust Design",
    "Helicopter RSM Simulation",

    # Implement Phase
    "Overview of the Implement Phase",
    "Prototype and Pilot, Process Control, Implementation Planning",
    "DMEDI Capstone"
]


import dspy

class GenerateFastApiCrudEndpoint(dspy.Signature):
    """
    Perfect Enterprise Quality NextJS 14 CRUD for a Design for Lean Six Sigma System files and Pyhton SQLModel and TS ORM
    """
    # Input Fields
    # reference = dspy.InputField(desc="A brief description or context about the Lean Six Sigma system module.")
    dfss_module = dspy.InputField(desc="The specific Design for Lean Six Sigma module or concept for which CRUD endpoints are to be created.")

    # Output Field
    code = dspy.OutputField(desc="NextJS 14 ORM CRUD for a Design for Lean Six Sigma System",
                            prefix='```typescript\n// NextJS 14 CRUD for a Design for Lean Six Sigma System'
                                   '\n\n"use client"\n\nimport React, { useState } from \'react\';\n')


async def send_request_to_model(model_id: str, rate_limit: int, folder: str):
    delay = .25  # 60 / rate_limit  # Calculating delay based on rate limit (requests per minute)
    for _ in range(rate_limit):  # Simulate sending the maximum number of requests in a minute
        # Placeholder for actual request logic
        print(f"Request sent to {model_id}")
        await anyio.sleep(delay)  # Wait to respect the rate limit

        try:
            with dspy.context(lm=Groq(model=model_id, max_tokens=2000)):
                dfss = choice(dfss_black_belt_curriculum)
                # chatgpt = ChatGPTChromaDBRetriever(k=3).forward(dfss)

                # Get 2000 characters of code from the model
                # chatgpt = str(chatgpt)[:2000]

                pred = dspy.ChainOfThought(GenerateFastApiCrudEndpoint)(dfss_module=dfss)
                # pred = dspy.ChainOfThought(GenerateFastApiCrudEndpoint)(reference=chatgpt, dfss_module=dfss)

                # Remove ``` if it is the last line
                if pred.code.endswith("```"):
                    code = pred.code[:-3]
                else:
                    code = pred.code

                render(code, "{{ folder }}/{{ dfss | underscore }}_crud.ts", dfss=dfss, folder=folder)
        except Exception as e:
            print(e)


async def run_all_models_concurrently():
    # Create a directory to store the generated FastAPI CRUD endpoint code based on Zulu time
    zulu_time = f"{datetime.now():%Y-%m-%d_%H-%M-%S}"

    models = [
        {"id": "llama2-70b-4096", "rate_limit": 30},
        {"id": "mixtral-8x7b-32768", "rate_limit": 30},
        {"id": "gemma-7b-it", "rate_limit": 30},
    ]

    async with create_task_group() as task_group:
        for model in models:
            task_group.soonify(send_request_to_model)(
                model_id=model["id"],
                rate_limit=model["rate_limit"],
                folder=zulu_time
            )


# Adapted `main` function to use anyio for running the asynchronous entry point
async def main():
    await run_all_models_concurrently()


if __name__ == '__main__':
    anyio.run(main)
