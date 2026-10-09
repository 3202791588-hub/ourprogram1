from django.conf import settings
from django.db import models
class AnalyticsEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="analytics_events")
    session = models.ForeignKey("tests.TestSession", null=True, blank=True, on_delete=models.SET_NULL, related_name="analytics_events")
    event_name = models.CharField(max_length=80)
    properties = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
