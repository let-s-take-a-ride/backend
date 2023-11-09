# backend/core/celery.py
from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

# Usuń te linie:
from configurations import importer
importer.install()
# import configurations
# configurations.setup()

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'run_my_task': {
#         'task': 'core.tasks.my_task',
#         # 'schedule': crontab(hour='15', minute="5"),
#         # 'schedule': timedelta(seconds=45),
#
#         'schedule': timedelta(seconds=5),
#     }
# }
