from django.urls import path
from. import views

# URLConf
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("save-answers/", views.save_answers, name="save-answers"),
    path("save-draft/", views.save_draft, name="save-draft"),
    path("recover-password/", views.recover_password, name="recover-password"),
    # path("save-preferences/", views.save_preferences, name="save-preferences"),
    path("mark-as-best/", views.mark_as_best, name="mark-as-best"),
    path("delete-draft/", views.delete_draft, name="delete_draft"),
]
