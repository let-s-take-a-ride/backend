from celery import shared_task
from time import sleep
from notification.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()
@shared_task
def add(x, y):
    # sleep(5)
    return x + y


@shared_task
def my_task():
    print("To jest komunikat debugujący")
    return "task completed"


@shared_task
def send_greetings_message(user_id):
    user = User.objects.get(id=user_id)
    print(user)
    Notification.objects.create(user=user, message=f'siema {user.nickname} witaj w lets take a ride', is_read=False)
