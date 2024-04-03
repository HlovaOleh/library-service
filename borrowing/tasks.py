from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.utils import timezone

from borrowing.models import Borrowing
from borrowing.services import calculate_fine_amount
from notification.management.commands.run_telegram_bot import (
    send_notification
)
from notification.models import TelegramUser

logger = get_task_logger(__name__)


@shared_task(bind=True)
def check_overdue_task(self):
    borrowings = Borrowing.objects.filter(
        expected_return_date__lte=timezone.now() + timezone.timedelta(days=1),
        is_active=True
    )
    users = set(borrowing.user.pk for borrowing in borrowings)

    for borrowing in borrowings:
        telegram_user = TelegramUser.objects.filter(
            user_id=borrowing.user.pk
        ).first()
        if telegram_user:
            borrowing_info = (
                "You have overdue borrowing:\n\n"
                f"-Book: {borrowing.book}\n"
                f"--Borrow date: {borrowing.borrow_date}\n"
                f"--Expected return date: {borrowing.expected_return_date}\n"
                f"--Amount to pay: {calculate_fine_amount(borrowing)}"
            )
            send_notification(
                telegram_user,
                borrowing_info
            )

    all_users = set(get_user_model().objects.values_list("pk", flat=True))
    users_with_borrowings = users.union(all_users)

    for user_id in all_users - users:
        telegram_user = TelegramUser.objects.filter(
            user_id=user_id
        ).first()
        if telegram_user:
            send_notification(
                telegram_user.chat_id,
                "No borrowings overdue today!"
            )
    return "Done sending notifications!"
