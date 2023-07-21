import requests
from django.shortcuts import render, redirect
import pyrebase

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
authe = firebase.auth()
db = firebase.database()


def register(request):
    if request.method == "POST":
        response = request.POST
        email = response["email"]
        password = response["password"]
        authe.create_user_with_email_and_password(email=email, password=password)
        user = authe.sign_in_with_email_and_password(email=email, password=password)

        ID = user["localId"]
        first_name = response["first name"]
        last_name = response["last name"]

        data = {
            "first-name": first_name,
            "last-name": last_name,
        }

        db.child("personal-data").child(ID).set(data)

        return render(request, "thankyou.html")


def login(request):
    if request.method == "POST":
        response = request.POST
        email = response["email"]
        password = response["password"]

        user = authe.sign_in_with_email_and_password(email=email, password=password)
        user_id = user["localId"]
        request.session["user_id"] = user_id

    return redirect("../../dashboard/")


def save_answers(request):
    if request.method == "POST":
        response = request.POST

        data = {}
        for key, value in response.items():
            if "question" in key:
                data[key] = value

        if request.session.get("user_id"):
            ID = request.session.get("user_id")

            db.child("user-answers").child(ID).set(data)

        return redirect("../../dashboard/")


def save_text(request):
    if request.method == "POST":
        response = request.POST
        text = response["text"]

        data = {"chapter 1": text}
        if request.session.get("user_id"):
            ID = request.session.get("user_id")

            db.child("user-book").child(ID).set(data)

        return redirect("../../dashboard/")


# ==================================================================================================================== #
# Helper functions
# ==================================================================================================================== #

def get_user_personal_data(user_id: str) -> dict:
    data = {
        "first_name": db.child('personal-data').child(user_id).child("first-name").get().val(),
        "last_name": db.child('personal-data').child(user_id).child("last-name").get().val()
    }
    return data


def get_questionnaire() -> dict:
    return dict(db.child("questions").get().val())


def get_user_answers(user_id) -> dict:
    return dict(db.child("user-answers").child(user_id).get().val())


def get_user_text(user_id) -> dict:
    return dict(db.child("user-book").child(user_id).get().val())


# For testing purposes
if __name__ == "__main__":
    pass
