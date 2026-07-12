from django.urls import path
from .views import UploadDocumentView, ChatView

urlpatterns = [
    # Upload PDF
    path("upload/", UploadDocumentView.as_view(), name="upload-document"),

    # Ask Question
    path("chat/", ChatView.as_view(), name="chat"),
]