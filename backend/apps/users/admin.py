from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class DemoUserAdmin(UserAdmin):
    list_display = ("id", "username", "openid", "status", "last_active_at")
    search_fields = ("username", "openid", "nickname")
    readonly_fields = ("date_joined", "last_login", "last_active_at")
