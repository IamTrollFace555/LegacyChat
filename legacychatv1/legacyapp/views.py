from django.shortcuts import render, redirect
from .modules.GPT.openai_API import generate_chapter
from fireapp.views import (
    get_user_personal_data,
    get_questionnaire,
    get_user_answers,
    get_user_book_chapter,
    consume_chapter_token,
    get_user_dashboard_table,
    user_chapter_setup,
)

from .modules.titles import (
    TITLE_DICT,
    SHORT_NAMES,
    SUBCHAPTER_LIST,
    CH_DICT,
    SUBCHAPTER_QUESTIONS,

)

from random import random


# Create your views here.
def homepage(request):
    return render(request, "homepage.html")


def dashboard(request):
    if request.session.get("user_id"):
        user_id = request.session.get("user_id")
        data = get_user_personal_data(user_id)

        data["table"] = get_user_dashboard_table(user_id)
        data["names"] = SHORT_NAMES

        return render(request, "dashboard.html", data)


def choose_subchapter(request):
    if request.method == "POST":
        response = request.POST
        chapter = response["chapter"]
        print("IM HEREEEEEEEEEEEEEEEEEEEEE")

        return render(
            request,
            "choose-subchapter.html",
            dict(subchapters=SUBCHAPTER_LIST[CH_DICT(chapter)],
                 counter=["sch" + str(i) for i in range(1, len(SUBCHAPTER_LIST[CH_DICT(chapter)]))],
                 chapter_name=TITLE_DICT[chapter],
                 chapter=chapter,
                 )
        )


def questionnaire(request):
    if request.method == "POST":
        response = request.POST
        chapter = str(response["chapter"])

        questions = get_questionnaire(chapter)

        try:
            subchapter = str(response["subchapter"])
            idxs = SUBCHAPTER_QUESTIONS[CH_DICT(chapter)][subchapter]

        except:
            idxs = [i for i in range(1, len(questions) + 1)]
            subchapter = "sch0"

        # Index managing
        indices = ""
        for i in idxs:
            indices += str(i) + " "
        indices = indices[:-1]


        try:
            ID = request.session.get("user_id")
            prev_answers = get_user_answers(ID, chapter)
            if prev_answers is None:
                raise Exception("")
        except:
            prev_answers = {}
            for idx in range(1, len(questions.items()) + 1):
                prev_answers[f"question{idx}"] = ""

        data = []
        for (key, value) in questions.items():
            temp = key[8:]  # Since the keys are in the form questionX where X is the question number, key[8:] just
            # removes the 'question' part
            try:
                prev = prev_answers[key]
            except:
                prev = ""
            data.append({"question_idx": temp, "question": value, "previous_answer": prev})

        if chapter != "0":
            subchapter_name = SUBCHAPTER_LIST[CH_DICT(chapter)][subchapter]
        else:
            subchapter_name = ""

        return render(
            request,
            "questionnaire.html",
            {"data": data,
             "chapter": chapter,
             "subchapter": subchapter,
             "chapter_name": TITLE_DICT[chapter],
             "subchapter_name": subchapter_name,
             "indices": indices,
             "indices_int": idxs}
        )


def chapter_edit(request):
    try:
        user_id = request.session.get("user_id")
        if request.method == "POST":
            response = request.POST
            chapter = response["chapter"]
            try:
                # Show the text stored in the database
                pages = get_user_book_chapter(user_id, chapter)
                if pages is None:
                    user_chapter_setup(user_id)
            except:
                # Consume a token and generate chapter
                if consume_chapter_token(user_id, chapter):
                    text = generate_chapter(user_id, chapter)
                else:
                    # Display error text if you
                    text = "Internal Error: You ran out of tokens!"

            return render(
                request,
                "edit.html",
                {"text": text, "chapter": chapter, "chapter_name": TITLE_DICT[chapter]})

    except:
        pass


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect("../../")


def summary(request):

    try:
        user_id = request.session.get("user_id")
        if request.method == "POST":
            response = request.POST
            chapter = response["chapter"]
            flag = ""

            try:
                questions = get_questionnaire(chapter)
                answers = get_user_answers(user_id, chapter)
                idxs = [f"question{i}" for i in range(1, len(questions) + 1)]
            except:
                flag = "Nothing here yet!"

            data = {"questions": questions, "answers": answers, "idxs": idxs, "flag": flag, "chapter_name": TITLE_DICT[chapter]}


            return render(
                request,
                "summary.html",
                data)

    except:
        pass

# ======================================= HELPER FUNCTIONS ======================================= #
def create_summary(user_id, chapter):

    user_data = get_user_personal_data(user_id)
    questions = get_questionnaire(chapter)

    first_name = user_data["first_name"]
    last_name = user_data["last_name"]

    filename = f"{first_name}_{last_name}.txt"
    with open(filename, "w") as file:
        pass


