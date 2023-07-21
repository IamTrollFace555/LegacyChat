from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .modules.GPT.GPT_request import get_response
import os
import json
import mimetypes


def home(request):
    return render(request, "index.html")


def questionnaire(request):
    return render(request, "questionnaire.html")


def submit_questionnaire(request):
    if request.method == "POST":
        response = request.POST
        name = response["name"]

        # Check if the user has already answered the questions
        files = os.listdir("playground/profiles/")
        if f"{name}.json" not in files:

            answers = dict()
            for question, answer in response.items():
                if question != "csrfmiddlewaretoken":
                    answers[question] = answer

            json_data = json.dumps({"responses": answers}, indent=2)

            # Save the JSON data to a file
            with open(f"{name}.json", "w") as file:
                file.write(json_data)

            os.rename(f"{name}.json", f"playground/profiles/{name}.json")

        with open(f"playground/profiles/current_user.txt", "w") as file:
            file.write(name)

    return HttpResponseRedirect(reverse("edit"))


def get_and_edit_text(request):
    with open(f"playground/profiles/current_user.txt", "r") as file:
        temp = file.readlines()
        name = "".join(temp)
        response = get_response(name)

    # response = "Hello World!"
    return render(request, "edit.html", {"text": response})

def save_text(request):
    if request.method == "POST":
        response = request.POST
        text = response["text"]

        # Get the current user
        with open(f"playground/profiles/current_user.txt", "r") as file:
            temp = file.readlines()
            name = "".join(temp)

        # Save the user's text to a file
        with open(f"playground/texts/{name}.txt", "w") as file:
            file.write(text)

        return HttpResponseRedirect(reverse("thankyou"))

def thankyou(request):
    return render(request, "thankyou.html")

def download(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    with open(f"playground/profiles/current_user.txt", "r") as file:
        temp = file.readlines()
        filename = "".join(temp) + ".txt"
    # Define the full file path
    filepath = BASE_DIR + '/playground/texts/' + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


