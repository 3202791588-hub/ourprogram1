from django.contrib import admin
from .models import PersonalityTemplate, ResultSnapshot, ResultUnlock
@admin.register(PersonalityTemplate)
class PersonalityTemplateAdmin(admin.ModelAdmin): list_display=("key","name","version","active"); list_filter=("active","version"); search_fields=("key","name")
@admin.register(ResultSnapshot)
class ResultSnapshotAdmin(admin.ModelAdmin): list_display=("id","user","result_type","test_version","scoring_version","created_at"); list_filter=("result_type","scoring_version"); search_fields=("user__openid","result_type"); readonly_fields=("created_at",)
@admin.register(ResultUnlock)
class ResultUnlockAdmin(admin.ModelAdmin): list_display=("user","result","unlock_type","created_at"); list_filter=("unlock_type",); readonly_fields=("created_at",)
