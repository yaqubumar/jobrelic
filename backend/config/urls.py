from django.contrib import admin
from django.urls import include, path

from apps.common.views import root_view

urlpatterns = [
    path("", root_view, name="root"),
    path("admin/", admin.site.urls),
    path("api/", include("apps.common.urls")),
    path("api/profile/", include("apps.profiles.urls")),
    path("api/jobs/", include("apps.jobs.urls")),
    path("api/", include("apps.applications.urls")),
]
