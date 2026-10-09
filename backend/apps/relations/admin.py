from django.contrib import admin
from .models import RelationInvite, RelationTemplate, Relationship, RelationshipReport
@admin.register(RelationTemplate)
class RelationTemplateAdmin(admin.ModelAdmin): list_display=("key","name","version","active"); list_filter=("active","version"); search_fields=("key","name")
@admin.register(RelationInvite)
class RelationInviteAdmin(admin.ModelAdmin): list_display=("invite_code","creator_user","accepted_user","status","created_at"); list_filter=("status",); search_fields=("invite_code","creator_user__openid"); readonly_fields=("created_at","accepted_at")
@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin): list_display=("id","user_a","user_b","relation_algorithm_version","created_at"); readonly_fields=("created_at",)
@admin.register(RelationshipReport)
class RelationshipReportAdmin(admin.ModelAdmin): list_display=("relationship","relation_type","compatibility_score","created_at"); list_filter=("relation_type",); readonly_fields=("created_at",)
