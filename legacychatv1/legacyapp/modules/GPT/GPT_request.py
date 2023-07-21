import openai
import json
import os
from fireapp.views import get_user_answers

openai.api_key = "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"


def create_prompt(user_id):
    with open("legacyapp/modules/GPT/prompt_template.txt", "r") as file:
        temp = file.readlines()
        prompt = "".join(temp)

    answers = get_user_answers(user_id)

    for key, value in answers.items():
        prompt += f"{key}: {value}\n"

    request = "\n\nWrite the book chapter based on the information provided to you"
    prompt += request

    return prompt


def get_response(name):
    prompt = create_prompt(name)
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=3000)
    generated_text = response["choices"][0]["message"]["content"]

    return generated_text


# if __name__ == "__main__":
#     print(get_response("Paola"))
