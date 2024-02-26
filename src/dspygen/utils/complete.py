from dataclasses import dataclass, field
from typing import Optional

import openai


@dataclass
class LLMConfig:
    prompt: str = ""
    model: str = "3i"
    temperature: float = 0.0
    max_tokens: int = 250
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[list[str]] = field(default=None)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid config key: {key}")


def create(config: Optional[LLMConfig] = None, **kwargs):
    if config:
        config.update(**kwargs)
        prompt = config.prompt
        model = config.model
        temperature = config.temperature
        max_tokens = config.max_tokens
        top_p = config.top_p
        frequency_penalty = config.frequency_penalty
        presence_penalty = config.presence_penalty
        stop = config.stop
    else:
        prompt = kwargs.get("prompt", "")
        model = kwargs.get("model", "3i")
        temperature = kwargs.get("temperature", 0)
        max_tokens = kwargs.get("max_tokens", 250)
        top_p = kwargs.get("top_p", 1)
        frequency_penalty = kwargs.get("frequency_penalty", 0)
        presence_penalty = kwargs.get("presence_penalty", 0)
        stop = kwargs.get("stop", None)

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )
    return response.choices[0].text.strip()


async def acreate(*, config: Optional[LLMConfig] = None, **kwargs):
    if config:
        config.update(**kwargs)
        prompt = config.prompt
        model = config.model
        temperature = config.temperature
        max_tokens = config.max_tokens
        top_p = config.top_p
        frequency_penalty = config.frequency_penalty
        presence_penalty = config.presence_penalty
        stop = config.stop
    else:
        prompt = kwargs.get("prompt", "")
        model = kwargs.get("model", "3i")
        temperature = kwargs.get("temperature", 0)
        max_tokens = kwargs.get("max_tokens", 250)
        top_p = kwargs.get("top_p", 1)
        frequency_penalty = kwargs.get("frequency_penalty", 0)
        presence_penalty = kwargs.get("presence_penalty", 0)
        stop = kwargs.get("stop", None)

    model = get_model(model)

    if model == "llama":
        from llama_cpp import Llama

        llm = Llama(
            model_path="/Users/candacechatman/dev/models/codellama-7b.Q4_0.gguf"
        )

        response = llm(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
        )
        print(response)
        choice = response["choices"][0]
        return choice["text"]

    if model == "chatgpt":
        return await goto_chatgpt(prompt)

    else:
        response = await client.completions.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
        )

        return response.choices[0].text.strip()


import asyncio
import json
import os
from dataclasses import dataclass
from time import sleep
from typing import Union

from loguru import logger

# from fgn.completion.prompt_schemas import *
# from fgn.utils.llama_llm import LocalLlamaClient
# from fgn.utils.llm_operations import generate_filename
DEFAULT_PROMPT = ""
DEFAULT_SYS_MSG = "AI chatbot that converses like a LLM 7 AGI Hive-Mind simulator"
DEFAULT_MODEL = "4"
DEFAULT_MAX_RETRY = 5
DEFAULT_BACKOFF_FACTOR = 2
DEFAULT_INITIAL_WAIT = 1


def chat(
    prompt=DEFAULT_PROMPT,
    sys_msg=DEFAULT_SYS_MSG,
    msgs=None,
    funcs=None,
    model=DEFAULT_MODEL,
    max_retry=DEFAULT_MAX_RETRY,
    backoff_factor=DEFAULT_BACKOFF_FACTOR,
    initial_wait=DEFAULT_INITIAL_WAIT,
    raw_msg=False,
    write_path=None,
    mode="a+",
) -> Union[str, dict]:
    """Customized completion function that interacts with the OpenAI API, capable of handling prompts, system messages,
    and specific functions. If the content length is too long, it will shorten the content and retry.

    Parameters:
        prompt (str, optional): The initial prompt for the chat conversation.
        sys_msg (str, optional): System message to guide the model's behavior.
        msgs (List[dict], optional): Previous messages in the conversation.
        funcs (List[Callable], optional): Custom functions to be applied on the response.
        model (str, optional): The OpenAI model to be used for completion.
        max_retry (int, optional): Maximum number of retries in case of an error.
        backoff_factor (float, optional): Multiplicative factor for exponential backoff between retries.
        initial_wait (float, optional): Initial wait time for the exponential backoff.
        raw_msg (bool, optional): Whether to include raw message in the response.
        write_path (str, optional): Directory or file path to write the response.
        mode (str, optional): File opening mode if writing response to file.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = _create_messages(sys_msg, prompt, msgs)

    retry = 0

    model = get_model(model)

    while retry <= max_retry:
        try:
            params = _create_params(model, messages, funcs)
            res = None

            if str(model) == "2":
                ...
                # llama = LocalLlamaClient()
                # res = llama.complete(prompt=prompt)
            elif funcs:
                res = get_response(
                    openai.chat.completions.create(**params),
                    raw_msg=raw_msg,
                    funcs=funcs,
                )
            else:
                res = get_response(
                    openai.chat.completions.create(**params),
                    raw_msg=raw_msg,
                    funcs=funcs,
                )

            write_response(mode, prompt, res, write_path)

            return res
        except Exception as oops:
            logger.warning(oops)
            # If the error is due to maximum context length, chop the messages and retry
            if "maximum context length" in str(oops):
                messages = messages[:1] + messages[2:]
                # Reset the retry attempts
                retry = 0
                continue

            # Increment the retry attempts
            retry += 1

            # If reached the maximum retry attempts, return the error message
            if retry > max_retry:
                raise ValueError(
                    f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
                )

            # Calculate the waiting time for exponential backoff
            wait_time = initial_wait * (backoff_factor ** (retry - 1))

            # Print the error and wait before retrying
            logger.warning(
                f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
            )
            sleep(wait_time)


# Callable class version of chat using dataclass
@dataclass
class Chat:
    prompt = DEFAULT_PROMPT
    sys_msg = DEFAULT_SYS_MSG
    msgs = None
    funcs = None
    model = DEFAULT_MODEL
    max_retry = DEFAULT_MAX_RETRY
    backoff_factor = DEFAULT_BACKOFF_FACTOR
    initial_wait = DEFAULT_INITIAL_WAIT
    raw_msg = False

    def __call__(self, **kwargs):
        return chat(**kwargs)


async def achat(
    prompt=DEFAULT_PROMPT,
    sys_msg=DEFAULT_SYS_MSG,
    msgs=None,
    funcs=None,
    model=DEFAULT_MODEL,
    max_retry=DEFAULT_MAX_RETRY,
    backoff_factor=DEFAULT_BACKOFF_FACTOR,
    initial_wait=DEFAULT_INITIAL_WAIT,
    raw_msg=False,
    write_path=None,
    mode="a+",
) -> Union[str, dict]:
    """Customized completion function that interacts with the OpenAI API, capable of handling prompts, system messages,
    and specific functions. If the content length is too long, it will shorten the content and retry.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = _create_messages(sys_msg, prompt, msgs)

    if funcs is None:
        funcs = []

    # Initialize retry attempts
    retry = 0

    # Run the loop for retry attempts
    while retry <= max_retry:
        try:
            params = _create_params(model, messages, funcs)
            res = None

            if funcs:
                res = get_response(
                    await AsyncCompletions.chat.completions.create(**params),
                    raw_msg=raw_msg,
                    funcs=funcs,
                )
            else:
                res = get_response(
                    await openai.chat.completions.create(**params),
                    raw_msg=raw_msg,
                    funcs=funcs,
                )

            await awrite_response(mode, prompt, res, write_path)

            return res
        except Exception as oops:
            logger.warning(oops)
            # If the error is due to maximum context length, chop the messages and retry
            if "maximum context length" in str(oops):
                messages = messages[:1] + messages[2:]
                # Reset the retry attempts
                retry = 0
                continue

            retry += 1

            if retry > max_retry:
                raise ValueError(
                    f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
                )

            wait_time = initial_wait * (backoff_factor ** (retry - 1))

            print(
                f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
            )
            await asyncio.sleep(wait_time)


def write_response(mode, prompt, res, write_path):
    if write_path and os.path.isdir(write_path):
        # name = generate_filename(prompt)
        # logger.info(f"Creating file {name} in {write_path}")
        # write_path = os.path.join(write_path, generate_filename(prompt))
        pass
    if write_path:
        with open(write_path, mode) as f:
            f.write(f"{res}\n")


async def awrite_response(mode, prompt, res, write_path):
    if write_path and os.path.isdir(write_path):
        # name = generate_filename(prompt)
        # logger.info(f"Creating file {name} in {write_path}")
        # write_path = os.path.join(write_path, generate_filename(prompt))
        pass
    if write_path:
        with open(write_path, mode) as f:
            f.write(f"{res}\n")


def get_response(res, raw_msg, funcs):
    msg = res.get("choices")[0].get("message")

    if raw_msg:
        return msg

    func = msg.get("function_call")

    if func:
        try:
            func["arguments"] = json.loads(func.get("arguments", ""))
        except json.decoder.JSONDecodeError:
            pass
        # if it is not a valid json, {"name": "func_name", "arguments": {}}, throw a error
        if not isinstance(func, dict) or not isinstance(func.get("arguments"), dict):
            error_msg = f"Invalid function response from OpenAI API {msg}"
            logger.exception(error_msg)
            raise ValueError(error_msg)
        else:
            return func
    elif funcs and len(funcs) > 0:
        error_msg = f"Invalid function response from OpenAI API {msg}"
        logger.exception(error_msg)
        raise ValueError(error_msg)
    else:
        return msg.get("content", "").strip()


def _create_params(model, messages, funcs=None):
    parameters = {
        "model": get_model(model),
        "messages": messages,
    }
    if funcs:
        parameters["functions"] = funcs
        parameters["function_call"] = "auto"

    return parameters


def _create_messages(sys_msg, prompt, msgs):
    messages = []

    if msgs is None:
        messages = [
            {"role": "system", "content": sys_msg},
        ]

    if prompt:
        messages.append({"role": "user", "content": prompt})

    # Extend the messages list with the provided prompt, system message, and previous messages
    if msgs:
        messages.extend(msgs)

    return messages
