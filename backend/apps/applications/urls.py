from django.urls import path

from .api import dashboard

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
]
