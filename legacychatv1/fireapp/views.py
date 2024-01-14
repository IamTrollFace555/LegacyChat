import requests
from django.shortcuts import render, redirect
import pyrebase
import warnings

QUESTIONNAIRE_DICT = {
    "0": "profile",
    "1": "Chapter 1: The Early Years: Foundations of a Life",
    "2": "Chapter 2: Teenage Revelations: Navigating Change and Discovery",
    "3": "Chapter 3: Into Adulthood: The Awakening of Purpose",
    "4": "Chapter 4: Personal Milestones: Love, Family, and Personal Growth",
    "5": "Chapter 5: Mature Reflections: A Lifetime of Lessons Learned",
    "6": "Chapter 6: Golden Years: Embracing Wisdom and Legacy",
}

CH_DICT = lambda x: "ch" + x if x != "0" else "profile"

# ==================================================================================================================== #
# Views
# ==================================================================================================================== #
config = {
    "apiKey": "AIzaSyARWU7n1tQjbHWpImgk1ymmfUhe3jrVZj8",
    "authDomain": "legacychat-v1-411213.firebaseapp.com",
    "databaseURL": "https://legacychat-v1-411213-default-rtdb.firebaseio.com",
    "projectId": "legacychat-v1-411213",
    "storageBucket": "legacychat-v1-411213.appspot.com",
    "messagingSenderId": "310084659311",
    "appId": "1:310084659311:web:66a80fe7e8ac8d22c6c59a"
}

# here we are doing firebase authentication
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


def register(request):
    if request.method == "POST":
        response = request.POST
        email = response["email"]
        password = response["password"]

        # Create user
        try:
            auth.create_user_with_email_and_password(email=email, password=password)

        # if the user already exists
        except:
            return redirect("../../users/register")

        # Log the user in
        user = auth.sign_in_with_email_and_password(email=email, password=password)

        ID = user["localId"]
        first_name = response["first name"]
        last_name = response["last name"]

        data = {
            "first-name": first_name,
            "last-name": last_name,
            "completed-chapters": {
                "profile": False,
                "ch1": False,
                "ch2": False,
                "ch3": False,
                "ch4": False,
                "ch5": False,
                "ch6": False,
            },
            "chapter-tokens": {
                "profile": 0,
                "ch1": 0,
                "ch2": 0,
                "ch3": 0,
                "ch4": 0,
                "ch5": 0,
                "ch6": 0,
            },
            "chosen-option": {
                "ch1": 1,
                "ch2": 1,
                "ch3": 1,
                "ch4": 1,
                "ch5": 1,
                "ch6": 1,
            },
        }

        db.child("personal-data").child(ID).set(data)

        return render(request, "thankyou.html")


def login(request):
    if request.method == "POST":
        response = request.POST
        email = response["email"]
        password = response["password"]

        # Try to log in
        try:
            user = auth.sign_in_with_email_and_password(email=email, password=password)
            user_id = user["localId"]
            request.session["user_id"] = user_id
        except:
            return redirect("../../users/login")

    return redirect("../../dashboard/")


def recover_password(request):
    if request.method == "POST":
        response = request.POST
        email = response["email"]

        auth.send_password_reset_email(email)

    return render(request, "recovery_email_sent.html")


def save_answers(request):
    if request.method == "POST":
        response = request.POST
        chapter = response["chapter"]

        data = {}

        completed = True
        for key, value in response.items():
            if "question" in key:
                data[key] = value
                # Check if there is a question that hasn't been answered yet
                if value == "":
                    completed = False

        if request.session.get("user_id"):
            ID = request.session.get("user_id")
            db.child("user-answers").child(ID).child(QUESTIONNAIRE_DICT[chapter]).update(data)

            if completed:
                db.child("personal-data").child(ID).child("completed-chapters").child(CH_DICT(chapter)).set(True)
            else:
                db.child("personal-data").child(ID).child("completed-chapters").child(CH_DICT(chapter)).set(False)

        try:
            if response["generate"] == "True":
                request.session['chapter'] = chapter
                request.session['failed'] = False
                return redirect("../../dashboard/chapter-edit/")

        except:
            pass

        return redirect("../../dashboard/")


def save_draft(request):
    if request.method == "POST":
        response = request.POST
        draft = response["draft"]
        draft_num = response["draft_num"]
        chapter = response["chapter"]

        data = {"text": draft}
        user_id = request.session.get("user_id")

        db.child("user-book").child(user_id).child(CH_DICT(chapter)).child(f"gen{draft_num}").update(data)
        request.session['chapter'] = chapter

        return redirect("../../dashboard/book-drafting")


def save_preferences(request):
    if request.method == "POST":
        response = request.POST
        data = {}
        for i in range(1, 7):
            data[f"ch{i}"] = response[f"ch{i}"]

        if request.session.get("user_id"):
            user_id = request.session.get("user_id")
            db.child("personal-data").child(user_id).child("chosen-option").update(data)

        print("DATA: ", data)

        return redirect("../../dashboard/")


def mark_as_best(request):
    user_id = request.session.get("user_id")
    if request.method == "POST":
        response = request.POST
        chapter = response["chapter"]
        draft_num = response["draft_num"]

        pages = get_user_book_chapters(user_id, chapter)
        request.session['chapter'] = chapter

        for key, info in pages.items():
            db.child("user-book").child(user_id).child(CH_DICT(chapter)).child(key).update(
                {"best": (key == f"gen{draft_num}")})

    return redirect("../../dashboard/book-drafting")


def delete_draft(request):
    user_id = request.session.get("user_id")
    if request.method == "POST":
        response = request.POST
        chapter = response["chapter"]
        draft_num = response["draft_num"]
        request.session['chapter'] = chapter

        db.child("user-book").child(user_id).child(CH_DICT(chapter)).child(f"gen{draft_num}").remove()

    return redirect("../../dashboard/book-drafting")


# ==================================================================================================================== #
# Helper functions
# ==================================================================================================================== #

def get_user_personal_data(user_id: str) -> dict or None:
    try:
        data = dict(db.child('personal-data').child(user_id).get().val())
        data["first_name"] = data["first-name"]
        data["last_name"] = data["last-name"]
        return data
    except:
        return None


def get_questionnaire(chapter) -> dict or None:
    try:
        return dict(db.child("questionnaires").child(QUESTIONNAIRE_DICT[chapter]).get().val())
    except:
        return None


def get_user_answers(user_id, chapter) -> dict or None:
    try:
        return dict(db.child("user-answers").child(user_id).child(QUESTIONNAIRE_DICT[chapter]).get().val())
    except:
        return None


def get_user_book_chapters(user_id, chapter) -> dict or None:
    try:
        return dict(db.child("user-book").child(user_id).child(CH_DICT(chapter)).get().val())
    except:
        return None


# def user_chapter_setup(user_id) -> bool:
#     try:
#         NUM_CHAPTERS = 6
#         data = {}
#
#         for i in range(NUM_CHAPTERS + 1):
#             temp = {"gen1": {"text": "", "creativity": "", "tone": "", "level": "", },
#                     "gen2": {"text": "", "creativity": "", "tone": "", "level": "", },
#                     "gen3": {"text": "", "creativity": "", "tone": "", "level": "", },
#                     }
#
#             data[CH_DICT(str(i))] = temp
#
#         db.child("user-book").child(user_id).set(data)
#         return True
#
#     except warnings.warn("Chapter setup failed!"):
#         return False


def consume_chapter_token(user_id, chapter):
    available_tokens = db.child("personal-data").child(user_id).child("chapter-tokens").child(
        CH_DICT(chapter)).get().val()

    if available_tokens == 0:
        return False

    db.child("personal-data").child(user_id).child("chapter-tokens").child(CH_DICT(chapter)).set(available_tokens - 1)

    return True


def get_user_dashboard_table(user_id):
    # Pictures

    data = {
        "chapter0": {"pictures": 0},
        "chapter1": {"pictures": 0},
        "chapter2": {"pictures": 0},
        "chapter3": {"pictures": 0},
        "chapter4": {"pictures": 0},
        "chapter5": {"pictures": 0},
        "chapter6": {"pictures": 0},
    }

    for chapter in range(len(QUESTIONNAIRE_DICT)):
        ch = str(chapter)

        # Questions
        answers = get_user_answers(user_id, ch)

        if answers is None:
            data[f"chapter{ch}"]["questions"] = "Go"
            started = False

        else:
            # Check answers and decide status based on them
            started = False
            finished = True

            for ans in answers.values():
                if ans == "":
                    finished = False
                else:
                    started = True

            if finished:
                data[f"chapter{ch}"]["questions"] = "Complete"
            elif started:
                data[f"chapter{ch}"]["questions"] = "Partial"
            else:
                data[f"chapter{ch}"]["questions"] = "Go"

        # Chapter Draft
        try:
            texts = get_user_book_chapters(user_id, ch)
            texts = [texts["gen1"]["text"], texts["gen2"]["text"], texts["gen3"]["text"]]
        except:
            texts = ["", "", ""]

        try:
            texts.index("")
            text = ""
        except:
            text = "Not empty!"

        if text is None or text == "":
            if started:
                data[f"chapter{ch}"]["draft"] = "Ready to write"
            else:
                data[f"chapter{ch}"]["draft"] = "Waiting answers"
        else:
            data[f"chapter{ch}"]["draft"] = "Complete"

    return data


def set_generated_chapter(user_id, chapter, text, params, gen_idx):
    data = {"text": text,
            "creativity": params["creativity"],
            "prompt": params["prompt"],
            "timestamp": params["timestamp"],
            "best": params["best"],
            "draft_num": params["draft_num"],
            }

    db.child("user-book").child(user_id).child(CH_DICT(chapter)).child(f"gen{gen_idx}").update(data)


def save_edited_chapter(user_id, chapter, gen, text):
    db.child("user-book").child(user_id).child(CH_DICT(chapter)).child(f"gen{gen}").update({"text": text})


def setup_chapter_answers(user_id, chapter):
    data = {}

    for c in range(1, 7):
        for i in range(1, 21):
            data[f"question{i}"] = ""

        db.child("user-answers").child(user_id).child(QUESTIONNAIRE_DICT[chapter]).update(data)


def add_token(user_id, chapter) -> int:
    token_count = db.child("personal-data").child(user_id).child("chapter-tokens").child(
        CH_DICT(chapter)).get().val()

    db.child("personal-data").child(user_id).child("chapter-tokens").child(CH_DICT(chapter)).set(token_count + 1)

    return token_count + 1


def get_token_amount(user_id, chapter) -> None:
    return db.child("personal-data").child(user_id).child("chapter-tokens").child(
        CH_DICT(chapter)).get().val()


# For testing purposes
if __name__ == "__main__":
    pass
