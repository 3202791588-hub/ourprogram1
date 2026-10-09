from django.conf import settings
from django.db import models

class RelationTemplate(models.Model):
    key = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    version = models.CharField(max_length=40, default="mock-v1")
    payload = models.JSONField(default=dict)
    active = models.BooleanField(default=True)
    def __str__(self) -> str: return self.name

class RelationInvite(models.Model):
    class Status(models.TextChoices): CREATED="CREATED"; OPENED="OPENED"; ACCEPTED="ACCEPTED"; COMPLETED="COMPLETED"; EXPIRED="EXPIRED"
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_invites")
    creator_result = models.ForeignKey("results.ResultSnapshot", on_delete=models.CASCADE, related_name="invites")
    invite_code = models.CharField(max_length=96, unique=True)
    status = models.CharField(max_length=16, choices=Status, default=Status.CREATED)
    accepted_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="accepted_invites")
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

class Relationship(models.Model):
    user_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="relationships_as_a")
    user_b = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="relationships_as_b")
    result_a = models.ForeignKey("results.ResultSnapshot", on_delete=models.PROTECT, related_name="relationships_as_a")
    result_b = models.ForeignKey("results.ResultSnapshot", on_delete=models.PROTECT, related_name="relationships_as_b")
    invite = models.OneToOneField(RelationInvite, on_delete=models.PROTECT, related_name="relationship")
    relation_algorithm_version = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

class RelationshipReport(models.Model):
    relationship = models.OneToOneField(Relationship, on_delete=models.CASCADE, related_name="report")
    relation_type = models.CharField(max_length=60)
    compatibility_score = models.PositiveSmallIntegerField()
    dimension_scores = models.JSONField(default=dict)
    report_payload = models.JSONField(default=dict)
    relation_algorithm_version = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
