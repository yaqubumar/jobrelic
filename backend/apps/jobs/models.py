from django.db import models


class JobPosting(models.Model):
    source = models.CharField(max_length=50, default="adzuna")
    external_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    employment_type = models.CharField(max_length=100, blank=True)
    application_url = models.URLField()
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    currency = models.CharField(max_length=10, default="GBP")
    source_payload = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("source", "external_id")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} @ {self.company}"
