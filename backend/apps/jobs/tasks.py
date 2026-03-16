from celery import shared_task

from .adapters import get_adzuna_client
from .models import JobPosting


@shared_task
def fetch_adzuna_jobs(keyword: str = "software engineer") -> int:
    client = get_adzuna_client()
    jobs = client.fetch_jobs(keyword=keyword)

    created_or_updated = 0
    for item in jobs:
        defaults = {
            "title": item.get("title", "Untitled role"),
            "company": item.get(
                "company",
                {},
            ).get("display_name", "Unknown company"),
            "location": item.get("location", {}).get("display_name", ""),
            "description": item.get("description", ""),
            "requirements": item.get("description", ""),
            "employment_type": item.get("contract_time", ""),
            "application_url": item.get("redirect_url", "https://example.com"),
            "salary_min": item.get("salary_min"),
            "salary_max": item.get("salary_max"),
            "source_payload": item,
        }
        JobPosting.objects.update_or_create(
            source="adzuna",
            external_id=str(item.get("id")),
            defaults=defaults,
        )
        created_or_updated += 1

    return created_or_updated
