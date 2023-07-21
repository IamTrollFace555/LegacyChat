from django.shortcuts import render
from .modules.GPT.GPT_request import get_response
from fireapp.views import (
    get_user_personal_data,
    get_questionnaire,
    get_user_answers,
    get_user_text,
)


# Create your views here.
def homepage(request):
    return render(request, "homepage.html")


def dashboard(request):
    if request.session.get("user_id"):
        user_id = request.session.get("user_id")
        data = get_user_personal_data(user_id)
        return render(request, "dashboard.html", data)


def questionnaire(request):
    questions = get_questionnaire()

    try:
        ID = request.session.get("user_id")
        prev_answers = get_user_answers(ID)
    except:
        prev_answers = {}
        for idx in range(1, len(questions.items()) + 1):
            prev_answers[f"question{idx}"] = ""

    data = []
    for (key, value) in questions.items():
        temp = key[8:]
        prev = prev_answers[key]
        data.append({"question_idx": temp, "question": value, "previous_answer": prev})

    return render(request, "questionnaire.html", {"data": data})


def chapter_edit(request):
    try:
        ID = request.session.get("user_id")

        try:
            text = get_user_text(ID)["chapter 1"]
            return render(request, "edit.html", {"text": text})

        except:
            text = get_response(ID)
            return render(request, "edit.html", {"text": text})

    except:
        pass
