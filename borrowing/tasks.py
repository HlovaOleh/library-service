from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from borrowing.models import Borrowing

logger = get_task_logger(__name__)


@shared_task(bind=True)
def check_overdue_task(self):
    print("Doing stuff")
