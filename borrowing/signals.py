from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.management.commands.run_telegram_bot import (
    send_notification
)
from borrowing.models import Borrowing
from notification.models import TelegramUser


@receiver(post_save, sender=Borrowing)
def notify_new_borrowing(sender, instance, created, **kwargs):
    if created:
        try:
            borrowing_info = (
                "New borrowing created:\n\n"
                f"-Book: {instance.book}\n"
                f"--Borrow date: {instance.borrow_date}\n"
                f"--Expected return date: {instance.expected_return_date}\n"
            )
            send_notification(
                TelegramUser.objects.get(user_id=instance.user_id).chat_id,
                borrowing_info
            )
        except TelegramUser.DoesNotExist:
            pass
        except Exception as e:
            print(str(e))
