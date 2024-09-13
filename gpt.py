import openai
from enum import Enum

from flask import jsonify

with open("gpt.api", "r") as file:
    api_key = file.read().strip()

openai.api_key = api_key

openai.Model.list()


class GPTVersion(Enum):
    GPT_4_1106_PREVIEW = "gpt-4-1106-preview"
    GPT_4 = "gpt-4o-mini"
    GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT_3_5_TURBO = "gpt-3.5-turbo-1106"
    OFF = "off"


def chatgpt_not_available():
    return jsonify({"error": "This ChatGPT functionality is not available for your account"}), 403

def chatgpt_test(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        temperature=0.1
        # max_tokens=1000
    )

    return response


def chatgpt_single_request(message, gpt_version: GPTVersion, temperature=0.1, instructions=None):
    # Prepare the instructions if provided
    if instructions:
        instruction_message = {"role": "system", "content": instructions}
    else:
        instruction_message = None

    # Prepare the user message
    if isinstance(message, str):
        messages_to_send = [{"role": "user", "content": message}]
    elif isinstance(message, list):
        messages_to_send = [{"role": "user", "content": m} for m in message]
    else:
        raise ValueError("Input message should either be a string or a list of strings.")

    # Combine the instruction message with the user message
    if instruction_message:
        messages_to_send.insert(0, instruction_message)

    response = openai.ChatCompletion.create(
        model=gpt_version.value,
        messages=messages_to_send,
        temperature=temperature
    )
    return response['choices'][0]['message']['content']


def chatgpt_single_request_with_tokens(message, gpt_version: GPTVersion, temperature=0.1, instructions=None):
    # Prepare the instructions if provided
    if instructions:
        instruction_message = {"role": "system", "content": instructions}
    else:
        instruction_message = None

    # Prepare the user message
    if isinstance(message, str):
        messages_to_send = [{"role": "user", "content": message}]
    elif isinstance(message, list):
        messages_to_send = [{"role": "user", "content": m} for m in message]
    else:
        raise ValueError("Input message should either be a string or a list of strings.")

    # Combine the instruction message with the user message
    if instruction_message:
        messages_to_send.insert(0, instruction_message)

    response = openai.ChatCompletion.create(
        model=gpt_version.value,
        messages=messages_to_send,
        temperature=temperature
    )

    return {
        'content': response['choices'][0]['message']['content'],
        'tokens': response['usage']['total_tokens']
    }


def chatgpt_single_request_stream(message, gpt_version, temperature=0, system=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model=gpt_version.value,
        messages=messages,
        temperature=temperature,
        stream=True
    )

    return response


def chatgpt_stream(messages, temperature, gpt_version: GPTVersion):
    response = openai.ChatCompletion.create(
        model=gpt_version.value,
        messages=messages,
        temperature=temperature,
        stream=True
    )

    return response
