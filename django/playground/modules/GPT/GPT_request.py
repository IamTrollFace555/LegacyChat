import openai
import json
import os

openai.api_key = "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"


def create_prompt(name):
    with open("playground/modules/GPT/prompt_template.txt", "r") as file:
        temp = file.readlines()
        prompt = "".join(temp)

    with open(f"playground/profiles/{name}.json") as file:
        questions = json.load(file)["responses"]

    for question_key, question_text in questions.items():
        prompt += f"{question_key}: {question_text}\n"

    request = "\nMake a book chapter where you talk about the early years of your life"
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
