from __future__ import annotations

from django.core.mail import send_mail

from apps.jobs.models import JobPosting
from apps.jobs.services import calculate_match_score, serialize_job
from apps.profiles.models import CandidateProfile

from .models import JobApplication, SavedJob, SwipeEvent


def _send_confirmation_email(
    profile: CandidateProfile,
    job: JobPosting,
    method: str,
) -> None:
    send_mail(
        subject=f"Jobrelic {method.title()} application confirmation",
        message=(
            f"Hi {profile.user.username},\n\n"
            f"Your {method} application for {job.title} at "
            f"{job.company} has been queued.\n"
            f"Application link: {job.application_url}\n"
        ),
        from_email=None,
        recipient_list=[profile.user.email or "demo@jobrelic.local"],
        fail_silently=True,
    )


def create_application(
    profile: CandidateProfile,
    job: JobPosting,
    method: str,
) -> JobApplication:
    score = calculate_match_score(profile, job)
    application, created = JobApplication.objects.get_or_create(
        profile=profile,
        job=job,
        method=method,
        defaults={
            "status": JobApplication.Status.SUBMITTED,
            "match_score": score,
            "confirmation_email_sent": True,
            "submission_notes": (
                "Submission queued via adapter-ready application pipeline."
            ),
        },
    )
    if created:
        _send_confirmation_email(profile, job, method)
    return application


def queue_auto_applications(profile: CandidateProfile) -> int:
    if not profile.auto_apply_enabled:
        return 0

    created_count = 0
    for job in JobPosting.objects.filter(is_active=True):
        score = calculate_match_score(profile, job)
        if score >= profile.auto_apply_threshold:
            _, created = JobApplication.objects.get_or_create(
                profile=profile,
                job=job,
                method=JobApplication.Method.AUTO,
                defaults={
                    "status": JobApplication.Status.SUBMITTED,
                    "match_score": score,
                    "confirmation_email_sent": True,
                    "submission_notes": (
                        "Auto-applied via job match threshold workflow."
                    ),
                },
            )
            if created:
                _send_confirmation_email(profile, job, "auto")
                created_count += 1
    return created_count


def handle_swipe_action(
    profile: CandidateProfile,
    job: JobPosting,
    action: str,
) -> dict:
    SwipeEvent.objects.create(profile=profile, job=job, action=action)

    if action == SwipeEvent.Action.SAVE:
        SavedJob.objects.get_or_create(profile=profile, job=job)
        return {"status": "saved", "job": serialize_job(job)}
    if action == SwipeEvent.Action.APPLY:
        application = create_application(
            profile,
            job,
            JobApplication.Method.MANUAL,
        )
        return {
            "status": application.status,
            "job": serialize_job(job, score=application.match_score),
            "application_method": application.method,
        }
    return {"status": "skipped", "job": serialize_job(job)}


def get_dashboard(profile: CandidateProfile) -> dict:
    manual_applied = profile.applications.filter(
        method=JobApplication.Method.MANUAL
    ).count()
    auto_applied = profile.applications.filter(
        method=JobApplication.Method.AUTO
    ).count()
    saved_jobs = profile.saved_jobs.count()

    recent_applications = [
        {
            "job": application.job.title,
            "company": application.job.company,
            "method": application.method,
            "status": application.status,
            "match_score": application.match_score,
            "created_at": application.created_at.isoformat(),
        }
        for application in profile.applications.select_related("job")[:10]
    ]

    recent_saved = [
        {
            "job": saved.job.title,
            "company": saved.job.company,
            "saved_at": saved.created_at.isoformat(),
        }
        for saved in profile.saved_jobs.select_related("job")[:10]
    ]

    return {
        "stats": {
            "jobs_applied_for": manual_applied,
            "auto_applied_jobs": auto_applied,
            "saved_jobs": saved_jobs,
        },
        "recent_applications": recent_applications,
        "recent_saved_jobs": recent_saved,
    }
