from datetime import datetime, timedelta
from decimal import Decimal

import requests
from celery import shared_task

from monitors.models import Monitor, MonitorRequest


@shared_task(bind=True)
def task_monitor(self, monitor_id):

    try:

        monitor = Monitor.objects.get(pk=monitor_id)

        response = requests.get(monitor.endpoint, timeout=60)

        MonitorRequest.objects.create(
            response_time=int(response.elapsed.total_seconds() * 1000),
            response_status=response.status_code,
            monitor=monitor,
        )

    except Exception as e:
        print(str(e), type(e))
