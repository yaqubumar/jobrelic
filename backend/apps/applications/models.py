from django.db import models

from apps.jobs.models import JobPosting
from apps.profiles.models import CandidateProfile


class JobApplication(models.Model):
    class Method(models.TextChoices):
        AUTO = "auto", "Auto"
        MANUAL = "manual", "Manual"

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        SUBMITTED = "submitted", "Submitted"
        FAILED = "failed", "Failed"

    profile = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.QUEUED,
    )
    match_score = models.PositiveIntegerField(default=0)
    confirmation_email_sent = models.BooleanField(default=False)
    submission_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("profile", "job", "method")
        ordering = ["-created_at"]


class SavedJob(models.Model):
    profile = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="saved_jobs",
    )
    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name="saved_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile", "job")


class SwipeEvent(models.Model):
    class Action(models.TextChoices):
        APPLY = "apply", "Apply"
        SKIP = "skip", "Skip"
        SAVE = "save", "Save"

    profile = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="swipe_events",
    )
    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name="swipe_events",
    )
    action = models.CharField(max_length=20, choices=Action.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
