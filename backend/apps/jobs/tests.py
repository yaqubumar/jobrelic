from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.profiles.models import CandidateProfile

from .models import JobPosting
from .services import calculate_match_score

User = get_user_model()


class MatchingEngineTests(TestCase):
    def test_match_score_is_high_for_related_profile(self):
        user = User.objects.create_user(username="tester")
        profile = CandidateProfile.objects.create(
            user=user,
            headline="Python Django Engineer",
            summary=(
                "Build APIs with PostgreSQL, Redis, Celery, "
                "and JavaScript."
            ),
            skills=["python", "django", "postgresql", "redis", "celery"],
        )
        job = JobPosting.objects.create(
            source="adzuna",
            external_id="job-1",
            title="Senior Django Engineer",
            company="Example",
            location="Remote",
            description="Python, Django, PostgreSQL, Celery, and Redis role.",
            requirements="REST APIs and JavaScript UI collaboration.",
            application_url="https://example.com/jobs/1",
        )

        self.assertGreaterEqual(calculate_match_score(profile, job), 60)
