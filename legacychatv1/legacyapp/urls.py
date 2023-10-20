from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("dashboard/", views.dashboard2, name="dashboard"),
    path("dashboard/questionnaire/", views.questionnaire, name="questionnaire"),
    path("dashboard/chapter-edit/", views.chapter_edit, name="chapter-edit"),
    path("dashboard/logout/", views.logout, name="logout"),
    path("dashboard/choose-subchapter/", views.choose_subchapter, name="choose-subchapter"),
    path("dashboard/summary/", views.summary2, name="summary"),
    path("dashboard/summary/download-summary/", views.download_summary, name="download-summary"),
    path("dashboard/generate-chapter/", views.generate_chapter_testing, name="generate-chapter"),
    path("dashboard/save-answers/", views.save_answers, name="save-answers"),

    # TEMP
    path("dashboard2/", views.dashboard2, name="dashboard2"),
]
