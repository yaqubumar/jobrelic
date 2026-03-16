from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.profiles.api import _get_or_create_demo_profile
from apps.applications.services import (
    handle_swipe_action,
    queue_auto_applications,
)

from .models import JobPosting
from .services import calculate_match_score, serialize_job
from .tasks import fetch_adzuna_jobs


def _job_queryset() -> QuerySet[JobPosting]:
    return JobPosting.objects.filter(is_active=True)


@api_view(["GET"])
def list_jobs(_request):
    profile = _get_or_create_demo_profile()
    threshold = int(_request.query_params.get("match_threshold", 0))
    jobs = []
    for job in _job_queryset()[:50]:
        score = calculate_match_score(profile, job)
        if score >= threshold:
            jobs.append(serialize_job(job, score=score))
    jobs.sort(key=lambda item: item.get("match_score", 0), reverse=True)
    return Response({"results": jobs})


@api_view(["POST"])
def fetch_jobs(request):
    keyword = request.data.get("keyword", "software engineer")
    created_or_updated = fetch_adzuna_jobs.delay(keyword=keyword)
    return Response(
        {"task_id": created_or_updated.id, "status": "queued"},
        status=202,
    )


@api_view(["POST"])
def swipe_job(request, job_id: int):
    profile = _get_or_create_demo_profile()
    action = request.data.get("action")
    job = JobPosting.objects.get(pk=job_id)
    result = handle_swipe_action(profile=profile, job=job, action=action)
    return Response(result)


@api_view(["POST"])
def run_auto_apply(request):
    profile = _get_or_create_demo_profile()
    created_count = queue_auto_applications(profile)
    return Response({"queued_applications": created_count, "status": "ok"})
