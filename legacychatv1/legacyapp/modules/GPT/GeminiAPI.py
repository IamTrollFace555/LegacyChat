import google.generativeai as genai
import json
import os
from fireapp.views import get_user_answers, get_questionnaire, get_user_book_chapters
from ..titles import QUESTIONNAIRE_DICT
from .template import Template

genai.configure(api_key="AIzaSyBgPvB3z54B4nV6agduh29wO8wACifSHQM")


def generate_chapter_API(user_id, chapter, params=None):
    # Generate prompt

    questions = get_questionnaire(chapter)
    answers = get_user_answers(user_id, chapter)
    profile_questions = get_questionnaire("0")
    profile_answers = get_user_answers(user_id, "0")
    temp = Template()

    if chapter == "0":
        prompt = temp.profile_prompt(questions, answers, params=params)
    else:

        prompt = temp.chapter_prompt(QUESTIONNAIRE_DICT[chapter], questions, answers, profile_questions,
                                     profile_answers, params)

    # Make a call to the Open-AI API
    model = "gpt-3.5-turbo-16k"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=12000,
                                            temperature=float(params["creativity"]) * 0.2)
    generated_text = response["choices"][0]["message"]["content"]

    return generated_text


def generate_chapter_testing_API(user_id, chapter, params=None):
    # Generate prompt

    questions = get_questionnaire(chapter)
    answers = get_user_answers(user_id, chapter)
    profile_questions = get_questionnaire("0")
    profile_answers = get_user_answers(user_id, "0")
    temp = Template()

    prompt = temp.chapter_prompt_testing(questions, answers, params)

    # Make a call to the Open-AI API
    model = "gpt-3.5-turbo-16k"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=8000,
                                            temperature=float(params["temperature"]))
    generated_text = response["choices"][0]["message"]["content"]

    return generated_text
