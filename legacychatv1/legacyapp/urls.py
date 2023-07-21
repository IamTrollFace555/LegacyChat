from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/questionnaire/", views.questionnaire, name="questionnaire"),
    path("dashboard/chapter-edit/", views.chapter_edit, name="questionnaire"),
]
