from django.shortcuts import render


# Create your views here.
def register(request):
    # Check the origin of the request
    prev_page = request.META["HTTP_REFERER"]
    flag = ""
    if "/users/register/" in prev_page:
        flag = "An user with that email already exists!"

    return render(request, "register.html", {"flag": flag})


def login(request):
    prev_page = request.META["HTTP_REFERER"]
    flag = ""
    if "/users/login/" in prev_page:
        flag = "Incorrect email or password!"

    return render(request, "login.html", {"flag": flag})


def password_recovery(request):
    return render(request, "password_recovery.html")
