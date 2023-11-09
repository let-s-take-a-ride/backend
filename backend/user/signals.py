# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from notification.models import Notification
from core.tasks import send_greetings_message

User = get_user_model()
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # Notification(user=instance, message=f'siema {instance} witaj w lets take a ride', is_read=False)
        print(instance.id)
        send_greetings_message.apply_async((instance.id,), countdown=30)


