from django.urls import path

from .api import fetch_jobs, list_jobs, run_auto_apply, swipe_job

urlpatterns = [
    path("", list_jobs, name="jobs-list"),
    path("fetch/", fetch_jobs, name="jobs-fetch"),
    path("auto-apply/", run_auto_apply, name="jobs-auto-apply"),
    path("<int:job_id>/swipe/", swipe_job, name="jobs-swipe"),
]
