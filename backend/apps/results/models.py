from django.conf import settings
from django.db import models

class PersonalityTemplate(models.Model):
    key = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    version = models.CharField(max_length=40, default="mock-v1")
    payload = models.JSONField(default=dict)
    active = models.BooleanField(default=True)
    def __str__(self) -> str: return self.name

class ResultSnapshot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="results")
    session = models.OneToOneField("tests.TestSession", on_delete=models.CASCADE, related_name="result")
    result_type = models.CharField(max_length=60)
    test_version = models.PositiveIntegerField()
    scoring_version = models.CharField(max_length=40)
    result_template_version = models.CharField(max_length=40)
    dimension_scores = models.JSONField(default=dict)
    result_payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

class ResultUnlock(models.Model):
    class Type(models.TextChoices): FREE="FREE"; AD="AD"; ADMIN="ADMIN"; MOCK="MOCK"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="result_unlocks")
    result = models.ForeignKey(ResultSnapshot, on_delete=models.CASCADE, related_name="unlocks")
    unlock_type = models.CharField(max_length=12, choices=Type)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "result"], name="unique_result_unlock")]
