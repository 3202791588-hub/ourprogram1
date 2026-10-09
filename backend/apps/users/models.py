from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    openid = models.CharField(max_length=128, unique=True)
    unionid = models.CharField(max_length=128, null=True, blank=True)
    nickname = models.CharField(max_length=80, blank=True)
    avatar_url = models.URLField(blank=True)
    status = models.CharField(max_length=16, default="active")
    last_active_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.nickname or self.username or self.openid
