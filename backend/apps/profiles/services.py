from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

from pypdf import PdfReader

COMMON_SKILLS = {
    "python",
    "django",
    "javascript",
    "html",
    "css",
    "react",
    "sql",
    "postgresql",
    "redis",
    "celery",
    "aws",
    "docker",
    "git",
    "api",
    "testing",
}


def extract_cv_text(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        return ""

    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    return path.read_text(encoding="utf-8", errors="ignore")


def parse_cv_to_profile_data(raw_text: str) -> dict:
    lowered = raw_text.lower()
    detected_skills = sorted(
        skill for skill in COMMON_SKILLS if skill in lowered
    )
    years = [int(match) for match in re.findall(r"(\d+)\+?\s+years", lowered)]
    experience_years = max(years) if years else 0
    matches = Counter(re.findall(r"[a-zA-Z]{4,}", lowered)).most_common(15)
    top_terms = [word for word, _count in matches]
    summary = " ".join(raw_text.strip().split())[:400]

    return {
        "summary": summary,
        "skills": detected_skills,
        "experience_years": experience_years,
        "keywords": top_terms,
    }
