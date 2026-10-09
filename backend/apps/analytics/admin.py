from django.contrib import admin
from .models import AnalyticsEvent
@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin): list_display=("event_name","user","session","created_at"); list_filter=("event_name",); search_fields=("event_name","user__openid"); readonly_fields=("created_at",)
