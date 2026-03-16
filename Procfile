web: cd backend && gunicorn config.wsgi
worker: cd backend && celery -A config worker --loglevel=info
