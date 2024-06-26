from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.beat import crontab

# Set the default Django settings module for the "celery" program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")

app = Celery("library_service")
app.conf.enable_utc = False

app.conf.update(
    timezone="Europe/Kiev",
    result_backend="django-db",
    task_serializer="json",
    accept_content=["application/json"],
    result_serializer="json",
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace="CELERY" means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace="CELERY")

# Celery Beat Settings
app.conf.beat_schedule = {
    "check-overdue-task": {
        "task": "borrowing.tasks.check_overdue_task",
        "schedule": crontab(hour="8"),
    },
    "check-payment-session-expiry": {
        "task": "payment.tasks.verify_session_status",
        "schedule": crontab(minute="*/1"),
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
