from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
    )
    headline = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    skills = models.JSONField(default=list, blank=True)
    job_preferences = models.JSONField(default=dict, blank=True)
    auto_apply_enabled = models.BooleanField(default=True)
    auto_apply_threshold = models.PositiveIntegerField(default=85)
    cv_file = models.FileField(upload_to="cv/", blank=True, null=True)
    parsed_cv = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile<{self.user.username}>"
