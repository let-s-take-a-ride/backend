from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_notification_to_user
from .models import Notification

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        user_id = instance.user.id
        message = instance.message
        print(user_id)
        print(message)
        send_notification_to_user(user_id, message)
