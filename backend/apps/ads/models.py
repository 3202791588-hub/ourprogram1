from django.conf import settings
from django.db import models
class AdEvent(models.Model):
    class Event(models.TextChoices): LOAD="LOAD"; SHOW="SHOW"; COMPLETE="COMPLETE"; CLOSE="CLOSE"; ERROR="ERROR"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ad_events")
    result = models.ForeignKey("results.ResultSnapshot", on_delete=models.CASCADE, related_name="ad_events")
    event = models.CharField(max_length=12, choices=Event)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
