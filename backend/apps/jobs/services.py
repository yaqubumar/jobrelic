from __future__ import annotations

import re

from apps.profiles.models import CandidateProfile

from .models import JobPosting


def tokenize(*values: str) -> set[str]:
    tokens: set[str] = set()
    for value in values:
        tokens.update(re.findall(r"[a-zA-Z0-9+#.-]+", (value or "").lower()))
    return {token for token in tokens if len(token) > 2}


def calculate_match_score(profile: CandidateProfile, job: JobPosting) -> int:
    profile_tokens = tokenize(
        profile.headline,
        profile.summary,
        " ".join(profile.skills),
        " ".join(str(value) for value in profile.job_preferences.values()),
    )
    job_tokens = tokenize(
        job.title,
        job.description,
        job.requirements,
        job.location,
        job.company,
    )

    if not profile_tokens or not job_tokens:
        return 0

    overlap = len(profile_tokens & job_tokens)
    coverage = overlap / max(len(profile_tokens), 1)
    relevance = overlap / max(len(job_tokens), 1)
    score = (coverage * 0.65) + (relevance * 0.35)
    return round(score * 100)


def serialize_job(job: JobPosting, score: int | None = None) -> dict:
    payload = {
        "id": job.id,
        "source": job.source,
        "external_id": job.external_id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "requirements": job.requirements,
        "employment_type": job.employment_type,
        "application_url": job.application_url,
        "salary_min": (
            float(job.salary_min) if job.salary_min is not None else None
        ),
        "salary_max": (
            float(job.salary_max) if job.salary_max is not None else None
        ),
        "currency": job.currency,
        "is_active": job.is_active,
    }
    if score is not None:
        payload["match_score"] = score
    return payload
