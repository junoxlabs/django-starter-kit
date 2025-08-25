import dramatiq

from django.core.mail import send_mail
from django.conf import settings


@dramatiq.actor
def send_test_email(subject, message, recipient_list):
    """
    A simple task to send a test email.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
    )


@dramatiq.actor
def perform_long_running_task(task_name):
    """
    A task that simulates a long-running operation.
    """
    import time
    time.sleep(5)  # Simulate work
    print(f"Task {task_name} completed!")