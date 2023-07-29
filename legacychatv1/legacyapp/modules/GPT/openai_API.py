import openai
import json
import os
from fireapp.views import get_user_answers, get_questionnaire, get_user_book_chapter
from .template import Template


openai.api_key = "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"

def generate_chapter(user_id, chapter, traits=None):

    # Generate prompt
    questions = get_questionnaire(chapter)
    answers = get_user_answers(user_id, chapter)
    profile = get_user_book_chapter(user_id, chapter)
    temp = Template()

    if chapter == "0":
        prompt = temp.profile_prompt(questions, answers)
    else:
        QUESTIONNAIRE_DICT = {
            "0": "profile",
            "1": "Chapter 1: The Early Years: Foundations of a Life",
            "2": "Chapter 2: Teenage Revelations: Navigating Change and Discovery",
            "3": "Chapter 3: Into Adulthood: The Awakening of Purpose",
            "4": "Chapter 4: Personal Milestones: Love, Family, and Personal Growth",
            "5": "Chapter 5: Mature Reflections: A Lifetime of Lessons Learned",
            "6": "Chapter 6: Golden Years: Embracing Wisdom and Legacy",
        }
        prompt = temp.chapter_prompt(QUESTIONNAIRE_DICT[chapter], questions, answers, profile)

    # Make a call to the Open-AI API
    model = "gpt-3.5-turbo-16k"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=12000)
    generated_text = response["choices"][0]["message"]["content"]

    return generated_text