import json

from django.db import transaction
from django.shortcuts import render
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework import viewsets
from rest_framework.exceptions import APIException

from monitors.models import Monitor, MonitorRequest
from monitors.serializers import MonitorRequestSerializer, MonitorSerializer


class MonitorViewSet(viewsets.ModelViewSet):

    serializer_class = MonitorSerializer
    queryset = Monitor.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():

                instance = serializer.save()
                schedule, created = IntervalSchedule.objects.get_or_create(
                    every=instance.interval,
                    period=IntervalSchedule.SECONDS,
                )

                task = PeriodicTask.objects.create(
                    interval=schedule,
                    name=f"Monitor: {instance.endpoint}",
                    task="monitors.tasks.task_monitor",
                    kwargs=json.dumps(
                        {
                            "monitor_id": instance.id,
                        }
                    ),
                )
                instance.task = task
                instance.save()

        except Exception as e:
            raise APIException(str(e))

    def perform_destroy(self, instance):
        if instance.task is not None:
            instance.task.delete()
        return super().perform_destroy(instance)


class MonitorRequestViewSet(viewsets.ModelViewSet):

    serializer_class = MonitorRequestSerializer
    queryset = MonitorRequest.objects.all()
