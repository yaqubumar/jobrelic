from __future__ import annotations

import os

import requests


class AdzunaClient:
    base_url = "https://api.adzuna.com/v1/api/jobs"

    def __init__(self, country: str, app_id: str, app_key: str):
        self.country = country
        self.app_id = app_id
        self.app_key = app_key

    def is_configured(self) -> bool:
        return bool(self.app_id and self.app_key)

    def fetch_jobs(
        self,
        *,
        keyword: str = "software engineer",
        page: int = 1,
    ) -> list[dict]:
        if not self.is_configured():
            return self._fallback_jobs(keyword)

        response = requests.get(
            f"{self.base_url}/{self.country}/search/{page}",
            params={
                "app_id": self.app_id,
                "app_key": self.app_key,
                "results_per_page": 20,
                "what": keyword,
                "content-type": "application/json",
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("results", [])

    @staticmethod
    def _fallback_jobs(keyword: str) -> list[dict]:
        return [
            {
                "id": "sample-1",
                "title": f"{keyword.title()} Developer",
                "company": {"display_name": "FutureStack"},
                "location": {"display_name": "London, UK"},
                "description": (
                    "Build Django APIs, Celery workers, PostgreSQL schemas, "
                    "and responsive UI flows."
                ),
                "redirect_url": "https://example.com/jobs/sample-1",
                "contract_time": "full_time",
                "salary_min": 55000,
                "salary_max": 70000,
            },
            {
                "id": "sample-2",
                "title": "Python Automation Engineer",
                "company": {"display_name": "AutoHire"},
                "location": {"display_name": "Remote"},
                "description": (
                    "Automate hiring workflows with Python, REST APIs, Redis, "
                    "and asynchronous task queues."
                ),
                "redirect_url": "https://example.com/jobs/sample-2",
                "contract_time": "contract",
                "salary_min": 450,
                "salary_max": 600,
            },
        ]


def get_adzuna_client() -> AdzunaClient:
    return AdzunaClient(
        country=os.getenv("ADZUNA_COUNTRY", "gb"),
        app_id=os.getenv("ADZUNA_APP_ID", ""),
        app_key=os.getenv("ADZUNA_APP_KEY", ""),
    )
