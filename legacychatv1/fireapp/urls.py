from django.urls import path
from. import views

# URLConf
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("save-answers/", views.save_answers, name="save-answers"),
    path("save-text/", views.save_text, name="save-text"),
    path("recover-password/", views.recover_password, name="recover-password"),
]
