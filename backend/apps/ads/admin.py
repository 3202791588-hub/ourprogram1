from django.contrib import admin
from .models import AdEvent
@admin.register(AdEvent)
class AdEventAdmin(admin.ModelAdmin): list_display=("user","result","event","created_at"); list_filter=("event",); readonly_fields=("created_at",)
