import requests
from django.shortcuts import render, redirect
import pyrebase

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
    "apiKey": "AIzaSyDgRHq65LSjzQGEmntMQLFlXgMywblMALs",
    "authDomain": "legacychat-v1.firebaseapp.com",
    "databaseURL": "https://legacychat-v1-default-rtdb.firebaseio.com",
    "projectId": "legacychat-v1",
    "storageBucket": "legacychat-v1.appspot.com",
    "messagingSenderId": "833857418223",
    "appId": "1:833857418223:web:a72ca0275cd9263c967c1a"
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
                "ch1": 4,
                "ch2": 4,
                "ch3": 4,
                "ch4": 4,
                "ch5": 4,
                "ch6": 4,
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
            db.child("user-answers").child(ID).child(QUESTIONNAIRE_DICT[chapter]).set(data)

            if completed:
                db.child("personal-data").child(ID).child("completed-chapters").child(CH_DICT(chapter)).set(True)

        try:
            if response["exit"] == "false":
                r = requests.post('http://yourdomain/path/', data={'key': 'value'})
                return redirect("../../dashboard/questionnaire/", chapter=chapter)
        except:
            print("exception!")
        return redirect("../../dashboard/")


def save_text(request):
    if request.method == "POST":
        response = request.POST
        text = response["text"]
        chapter = response["chapter"]

        data = {CH_DICT(chapter): text}
        if request.session.get("user_id"):
            ID = request.session.get("user_id")

            db.child("user-book").child(ID).update(data)

        return redirect("../../dashboard/")


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


def get_user_book_chapter(user_id, chapter) -> str or None:
    try:
        return db.child("user-book").child(user_id).child(CH_DICT(chapter)).get().val()
    except:
        return None


def set_user_profile(user_id, profile):
    data = {"profile": profile}
    for idx in range(1, len(QUESTIONNAIRE_DICT)):
        data[CH_DICT(str(idx))] = ""

    db.child("user-book").child(user_id).set(data)


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
            finished = False

        else:
            # Check answers and decide status based on them
            started = False
            finished = True

            for ans in answers.values():
                print(ans)
                if ans == "":
                    finished = False
                    print("HEY THERE!")
                else:
                    started = True

            if finished:
                data[f"chapter{ch}"]["questions"] = "Complete"
            elif started:
                data[f"chapter{ch}"]["questions"] = "Partial"
            else:
                data[f"chapter{ch}"]["questions"] = "Go"

        # Chapter Draft
        text = get_user_book_chapter(user_id, ch)
        if text is None or text == "":
            if finished:
                data[f"chapter{ch}"]["draft"] = "Ready to write"
            else:
                data[f"chapter{ch}"]["draft"] = "Waiting answers"
        else:
            data[f"chapter{ch}"]["draft"] = "Complete"

    return data


# For testing purposes
if __name__ == "__main__":
    pass
