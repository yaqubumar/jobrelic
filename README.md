# Jobrelic

Jobrelic is an automated job application platform MVP with a Django backend, Celery task pipeline, PostgreSQL-ready persistence, and a static HTML/CSS/JavaScript frontend.

## MVP features

- Structured user profile with skills, experience, preferences, and CV parsing hooks
- Job ingestion pipeline with Adzuna integration and local fallback sample jobs
- Match engine that scores jobs against the candidate profile
- Auto-apply workflow for jobs meeting the configured threshold
- Swipe interface actions for apply, skip, and save
- Dashboard API for applied, auto-applied, and saved jobs
- Django admin for users, jobs, applications, and saved job activity

## Project structure

- `backend/`: Django project, apps, Celery config, tests, and admin setup
- `index.html`: Frontend shell for profile, swipe, and dashboard flows
- `assets/style.css`: Visual styling for the landing page and in-browser app
- `assets/app.js`: Frontend state, demo swipe interactions, and API integration hooks

## Backend apps

- `apps/profiles`: Candidate profile storage and CV parsing helpers
- `apps/jobs`: Adzuna fetch adapter, job storage, and similarity scoring
- `apps/applications`: Auto-apply pipeline, swipe handling, and dashboard data
- `apps/common`: Health endpoint and shared infrastructure helpers

## Environment variables

Copy `.env.example` to `.env` and update the values for your machine.

- `DATABASE_URL`: PostgreSQL connection string; falls back to SQLite for quick local bootstrap
- `REDIS_URL`: Celery broker and result backend
- `ADZUNA_APP_ID` / `ADZUNA_APP_KEY`: Adzuna API credentials
- `EMAIL_BACKEND`: Console email backend by default for local development

## Local development

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure the environment

```bash
cp .env.example .env
```

### 3. Run Django setup

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 4. Run Celery worker

```bash
cd backend
celery -A config worker --loglevel=info
```

### 5. Open the frontend

Serve the repo root with any static file server, then open `index.html` in your browser.

```bash
python3 -m http.server 5500
```

## Key API routes

- `GET /api/health/`
- `GET|POST /api/profile/`
- `POST /api/profile/parse-cv/`
- `GET /api/jobs/?match_threshold=85`
- `POST /api/jobs/fetch/`
- `POST /api/jobs/auto-apply/`
- `POST /api/jobs/<job_id>/swipe/`
- `GET /api/dashboard/`

## Notes

- Real third-party auto-submission usually requires per-board integrations and compliance review; this scaffold provides the orchestration pipeline and confirmation flow you can extend.
- The frontend ships with local demo data so the swipe experience works before the backend is fully populated.
- `Procfile` and `runtime.txt` are included for Heroku-style deployment.

