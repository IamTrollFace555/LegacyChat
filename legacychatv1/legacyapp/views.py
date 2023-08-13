from django.shortcuts import render
from .modules.GPT.openai_API import generate_chapter
from fireapp.views import (
    get_user_personal_data,
    get_questionnaire,
    get_user_answers,
    get_user_book_chapter,
    set_user_profile,
    consume_chapter_token,
    get_user_dashboard_table,
)

TITLE_DICT = {
    "0": "Building your profile",
    "1": "The Early Years: Foundations of a Life (Chapter 1)",
    "2": "Teenage Revelations: Navigating Change and Discovery (Chapter 2)",
    "3": "Into Adulthood: The Awakening of Purpose (Chapter 3)",
    "4": "Personal Milestones: Love, Family, and Personal Growth (Chapter 4)",
    "5": "Mature Reflections: A Lifetime of Lessons Learned (Chapter 5)",
    "6": "Golden Years: Embracing Wisdom and Legacy (Chapter 6)",
}


# Create your views here.
def homepage(request):
    return render(request, "homepage.html")


def dashboard(request):
    if request.session.get("user_id"):
        user_id = request.session.get("user_id")
        data = get_user_personal_data(user_id)

        # Generate person's profile if profile questions have been answered but it hasn't been generated yet
        if data["completed-chapters"]["profile"]:
            try:
                profile = get_user_book_chapter(user_id, "0")
                if profile == "" or profile is None:
                    text = generate_chapter(user_id, "0")
                    set_user_profile(user_id, text)
            except:
                text = generate_chapter(user_id, "0")
                set_user_profile(user_id, text)

        data["completed_chapters"] = data["completed-chapters"]
        data["chosen_option"] = data["chosen-option"]
        data["chapter_tokens"] = data["chapter-tokens"]

        data["table"] = get_user_dashboard_table(user_id)

        return render(request, "dashboard.html", data)


def questionnaire(request):
    if request.method == "POST":
        response = request.POST
        chapter = response["chapter"]

        questions = get_questionnaire(chapter)

        try:
            ID = request.session.get("user_id")
            prev_answers = get_user_answers(ID, chapter)
        except:
            prev_answers = {}
            for idx in range(1, len(questions.items()) + 1):
                prev_answers[f"question{idx}"] = ""

        data = []
        for (key, value) in questions.items():
            temp = key[
                   8:]  # Since the keys are in the form questionX where X is the question number, key[8:] just removes the 'question' part
            prev = prev_answers[key]
            data.append({"question_idx": temp, "question": value, "previous_answer": prev})

        return render(
            request,
            "questionnaire.html",
            {"data": data, "chapter": chapter, "chapter_name": TITLE_DICT[chapter]}
        )


def chapter_edit(request):
    try:
        ID = request.session.get("user_id")
        if request.method == "POST":
            response = request.POST
            chapter = response["chapter"]
            try:
                # Show the text stored in the database
                text = get_user_book_chapter(ID, chapter)
                if text is None or text == "":
                    raise Exception("")
            except:
                # Consume a token and generate chapter
                if consume_chapter_token(ID, chapter):
                    text = generate_chapter(ID, chapter)
                else:
                    # Display error text if you
                    text = "Internal Error: You ran out of tokens!"

            return render(
                request,
                "edit.html",
                {"text": text, "chapter": chapter, "chapter_name": TITLE_DICT[chapter]})

    except:
        pass
