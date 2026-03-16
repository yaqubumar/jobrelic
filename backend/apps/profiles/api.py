from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CandidateProfile
from .services import extract_cv_text, parse_cv_to_profile_data

User = get_user_model()


def _get_or_create_demo_profile():
    user, _ = User.objects.get_or_create(
        username="demo-user",
        defaults={"email": "demo@jobrelic.local"},
    )
    profile, _ = CandidateProfile.objects.get_or_create(user=user)
    return profile


def _serialize_profile(profile: CandidateProfile) -> dict:
    return {
        "id": profile.id,
        "username": profile.user.username,
        "email": profile.user.email,
        "headline": profile.headline,
        "summary": profile.summary,
        "location": profile.location,
        "experience_years": profile.experience_years,
        "skills": profile.skills,
        "job_preferences": profile.job_preferences,
        "auto_apply_enabled": profile.auto_apply_enabled,
        "auto_apply_threshold": profile.auto_apply_threshold,
        "parsed_cv": profile.parsed_cv,
    }


@api_view(["GET", "POST"])
def profile_detail(request):
    profile = _get_or_create_demo_profile()

    if request.method == "POST":
        payload = request.data
        profile.headline = payload.get("headline", profile.headline)
        profile.summary = payload.get("summary", profile.summary)
        profile.location = payload.get("location", profile.location)
        profile.experience_years = int(
            payload.get("experience_years", profile.experience_years or 0)
        )
        profile.skills = payload.get("skills", profile.skills)
        profile.job_preferences = payload.get(
            "job_preferences",
            profile.job_preferences,
        )
        profile.auto_apply_enabled = payload.get(
            "auto_apply_enabled",
            profile.auto_apply_enabled,
        )
        profile.auto_apply_threshold = int(
            payload.get("auto_apply_threshold", profile.auto_apply_threshold)
        )
        profile.save()

    return Response(_serialize_profile(profile))


@api_view(["POST"])
def parse_cv(request):
    profile = _get_or_create_demo_profile()
    file_path = request.data.get("file_path")

    if not file_path:
        return Response({"detail": "`file_path` is required."}, status=400)

    raw_text = extract_cv_text(file_path)
    parsed = parse_cv_to_profile_data(raw_text)

    profile.parsed_cv = parsed
    profile.summary = parsed.get("summary", profile.summary)
    profile.skills = parsed.get("skills", profile.skills)
    profile.experience_years = parsed.get(
        "experience_years",
        profile.experience_years,
    )
    profile.save()

    return Response(
        {
            "profile": _serialize_profile(profile),
            "source_length": len(raw_text),
        }
    )
