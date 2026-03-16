from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.jobs.models import JobPosting
from apps.profiles.models import CandidateProfile

from .models import JobApplication
from .services import create_application

User = get_user_model()


class ApplicationPipelineTests(TestCase):
    def test_manual_application_is_created(self):
        user = User.objects.create_user(
            username="demo",
            email="demo@example.com",
        )
        profile = CandidateProfile.objects.create(
            user=user,
            skills=["python", "django"],
        )
        job = JobPosting.objects.create(
            source="adzuna",
            external_id="job-2",
            title="Django Developer",
            company="Example Inc",
            description="Build Django applications.",
            requirements="Python and Django",
            application_url="https://example.com/jobs/2",
        )

        application = create_application(
            profile,
            job,
            JobApplication.Method.MANUAL,
        )

        self.assertEqual(application.method, JobApplication.Method.MANUAL)
        self.assertEqual(application.status, JobApplication.Status.SUBMITTED)
