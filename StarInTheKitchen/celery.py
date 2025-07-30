from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

import platform

if platform.system() == 'Windows':
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StarInTheKitchen.settings')

app = Celery('StarInTheKitchen')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

