from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/questionnaire/", views.questionnaire, name="questionnaire"),
    path("dashboard/chapter-edit/", views.chapter_edit, name="chapter-edit"),
    path("dashboard/logout/", views.logout, name="logout"),
    path("dashboard/choose-subchapter/", views.choose_subchapter, name="choose-subchapter"),
    path("dashboard/summary/", views.summary, name="summary"),
    path("dashboard/generate-chapter/", views.generate_chapter, name="generate-chapter"),

]
