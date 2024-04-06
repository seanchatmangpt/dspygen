from datetime import datetime
from random import choice

import anyio
import dspy
from asyncer import create_task_group
from pydantic import BaseModel, ValidationError

from dspygen.lm.groq_lm import Groq

from faker import Faker

from dspygen.modules.gen_pydantic_instance import get_model_source, eval_dict_str
from dspygen.utils.pydantic_tools import extract_valid_dicts

fake = Faker()

from dspygen.typetemp.functional import render


class Contact(BaseModel):
    name: str
    email: str
    phone: str

def generate_contact_str():
    return f"{fake.name()}, {fake.email()}, {fake.phone_number()}"

class Appointment(BaseModel):
    title: str
    description: str
    date_time: datetime
    contact: Contact

def generate_appointment_str():
    return f"{fake.sentence()}, on {fake.date(pattern='%Y-%m-%d %H:%M:%S')}"

    # print(generate_contact_str())
    # print(generate_appointment_str())

async def send_request_to_model(model_id: str, rate_limit: int, folder: str):
    source = get_model_source(Appointment)
    schema = Appointment.model_json_schema()

    # with dspy.context(lm=dspy.OpenAI(max_tokens=200)):
    with dspy.context(lm=Groq(model=model_id, max_tokens=200)):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        info = f"{generate_contact_str()} {generate_appointment_str()} {schema}"
        # print(f"info: {info}")

        pred = dspy.Predict("info -> valid_json")(info=info)
        model = pred.valid_json
        print(model)

        # print(f"model: {model_id}\n\n{model}\n\n")

        try:
            dicts = extract_valid_dicts(model.split("Valid Json:")[1])
            model_dict = dicts[0]
            inst = Contact.model_validate(model_dict)
            print(inst)
        except ValidationError as e:
            print(e)


async def run_all_models_concurrently():
    # Create a directory to store the generated FastAPI CRUD endpoint code based on Zulu time
    zulu_time = f"{datetime.now():%Y-%m-%d_%H-%M-%S}"

    models = [
        {"id": "llama2-70b-4096", "rate_limit": 30},
        # {"id": "mixtral-8x7b-32768", "rate_limit": 30},
        # {"id": "gemma-7b-it", "rate_limit": 30},
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