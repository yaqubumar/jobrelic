from django.urls import path

from .api import parse_cv, profile_detail

urlpatterns = [
    path("", profile_detail, name="profile-detail"),
    path("parse-cv/", parse_cv, name="profile-parse-cv"),
]
