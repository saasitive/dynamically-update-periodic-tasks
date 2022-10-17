from django.urls import re_path
from rest_framework.routers import DefaultRouter

from monitors.views import MonitorRequestViewSet, MonitorViewSet

router = DefaultRouter()
router.register(r"monitors", MonitorViewSet)
router.register(r"requests", MonitorRequestViewSet)
monitors_urlpatterns = router.urls
