import datetime
import random
from itertools import cycle

from pydantic import BaseModel

gpt_4_models = [
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
]

turbo_models = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
]

turbo_16k_models = [
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
]

models_returning_dict = [
    "gpt_3_5_turbo_instruct",
    "gpt_3_5_turbo_instruct_0914",
    "ada",
    "ada_similarity",
    "babbage",
    "babbage_002",
    "curie",
    "curie_instruct_beta",
    "curie_search_document",
    "curie_search_query",
    "curie_similarity",
    "davinci",
    "davinci_002",
    "davinci_instruct_beta",
    "text_ada_001",
    "text_babbage_001",
    "text_curie_001",
    "text_davinci_001",
    "text_davinci_002",
    "text_davinci_003",
    "text_search_curie_doc_001",
    "text_search_curie_query_001",
    "text_similarity_ada_001",
    "text_similarity_curie_001",
]

instruct_models = [
    "gpt-3.5-turbo-instruct",
    "gpt-3.5-turbo-instruct-0914",
]

# 4k max tokens
best_models = [
    "gpt-3.5-turbo-instruct",
    "gpt-3.5-turbo-instruct-0914",
    "text-davinci-003",
]

# 2k max tokens
ok_models = [
    "text-davinci-002",
    "davinci-instruct-beta",
    "curie-instruct-beta",
    "curie-similarity",
    "davinci-002",
    "text-curie-001",
    "text-similarity-curie-001",
]

all_models = [
    # "gpt_3_5_turbo",
    # "gpt_3_5_turbo_0301",
    # "gpt_3_5_turbo_0613",
    # "gpt_3_5_turbo_16k",
    # "gpt_3_5_turbo_16k_0613",
    "gpt_3_5_turbo_instruct",
    "gpt_3_5_turbo_instruct_0914",
    # "gpt_4",
    # "gpt_4_0314",
    # "gpt_4_0613",
    "ada",
    "ada_code_search_code",
    "ada_code_search_text",
    "ada_search_document",
    "ada_search_query",
    "ada_similarity",
    "babbage",
    "babbage_002",
    "babbage_code_search_code",
    "babbage_code_search_text",
    "babbage_search_document",
    "babbage_search_query",
    "babbage_similarity",
    "code_search_ada_code_001",
    "code_search_ada_text_001",
    "code_search_babbage_code_001",
    "code_search_babbage_text_001",
    "curie",
    "curie_instruct_beta",
    "curie_search_document",
    "curie_search_query",
    "curie_similarity",
    "davinci",
    "davinci_002",
    "davinci_instruct_beta",
    "davinci_search_document",
    "davinci_search_query",
    "davinci_similarity",
    "text_ada_001",
    "text_babbage_001",
    "text_curie_001",
    "text_davinci_001",
    "text_davinci_002",
    "text_davinci_003",
    "text_embedding_ada_002",
    "text_search_ada_doc_001",
    "text_search_ada_query_001",
    "text_search_babbage_doc_001",
    "text_search_babbage_query_001",
    "text_search_curie_doc_001",
    "text_search_curie_query_001",
    "text_search_davinci_doc_001",
    "text_search_davinci_query_001",
    "text_similarity_ada_001",
    "text_similarity_babbage_001",
    "text_similarity_curie_001",
    "text_similarity_davinci_001",
]


def round_robin_ok_models():
    models = cycle(ok_models)

    while True:
        yield next(models)


def round_robin_gpt_4_models():
    models = cycle(gpt_4_models)

    random.shuffle(gpt_4_models)

    while True:
        yield next(models)


def round_robin_instruct_models():
    models = cycle(instruct_models)

    while True:
        yield next(models)


def round_robin_best_models():
    models = cycle(best_models)

    while True:
        yield next(models)


def round_robin_turbo_models():
    models = cycle(turbo_models)

    while True:
        yield next(models)


def get_model(model):
    if model == "best":
        return next(round_robin_best_models())
    elif model == "ok":
        return next(round_robin_ok_models())
    elif model == "gpt4":
        return next(round_robin_gpt_4_models())
    elif model == "3":
        return "gpt-3.5-turbo-0613"
    elif model == "3i":
        return "gpt-3.5-turbo-instruct"
    elif model == "4":
        return "gpt-4-0613"
    elif model == "turbo":
        return next(round_robin_turbo_models())
    elif not model:
        return next(round_robin_instruct_models())
    else:
        return model


async def main():
    ...


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())


class User(BaseModel):
    name: str
    email: str


class Email(BaseModel):
    id: str
    subject: str
    body: str
    from_address: str
    to: list[str]
    cc: list[str] = []
    bcc: list[str] = []
    date: datetime.datetime


class MailingList(BaseModel):
    name: str
    members: list[User]
    emails: list[Email] = []


class UnixEmailSystem(BaseModel):
    hostname: str
    mailing_lists: list[MailingList] = []
    users: list[User] = []
