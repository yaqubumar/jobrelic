from django.urls import path

from .views import health_check, root_view

urlpatterns = [
    path("", root_view, name="root"),
    path("health/", health_check, name="health-check"),
]
