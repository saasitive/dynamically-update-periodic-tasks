# 
# celery -A backend worker --loglevel=info -P gevent --concurrency 1 -E
# celery -A backend beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --max-interval 60

import os
import sys
from celery import Celery

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CURRENT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
