from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path("dashboard/download-book/", views.download_book_pdf, name="download-book"),
    path("dashboard/book-drafting/", views.book_drafting, name="book-drafting"),
    # path("dashboard/upload-image/", views.upload_image, name="upload-image"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)