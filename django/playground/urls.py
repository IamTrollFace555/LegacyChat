from django.urls import path
from. import views

# URLConf
urlpatterns = [
    path("", views.home, name="home"),
    path("questionnaire/", views.questionnaire, name="questionnaire"),
    path("submit_questionnaire/", views.submit_questionnaire, name="submit_questionnaire"),
    path("edit/", views.get_and_edit_text, name="edit"),
    path("save_text/", views.save_text, name="save_text"),
    path("thankyou/", views.thankyou, name="thankyou"),
    path("download/", views.download, name="download"),
]
