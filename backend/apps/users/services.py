from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .adapters import get_wechat_auth_adapter
from .models import User

@transaction.atomic
def login(payload: dict) -> dict:
    identity = get_wechat_auth_adapter().exchange(payload)
    user, _ = User.objects.get_or_create(openid=identity.openid, defaults={"username": identity.openid, "nickname": identity.nickname})
    user.last_active_at = timezone.now(); user.save(update_fields=["last_active_at"])
    return {"access_token": str(RefreshToken.for_user(user).access_token), "user": {"id": user.id, "nickname": user.nickname}}

@transaction.atomic
def delete_user_data(user: User) -> None:
    from apps.ads.models import AdEvent
    from apps.analytics.models import AnalyticsEvent
    from apps.relations.models import RelationInvite, Relationship
    from apps.results.models import ResultUnlock
    AdEvent.objects.filter(user=user).delete(); AnalyticsEvent.objects.filter(user=user).delete(); ResultUnlock.objects.filter(user=user).delete()
    Relationship.objects.filter(user_a=user).delete(); Relationship.objects.filter(user_b=user).delete()
    RelationInvite.objects.filter(accepted_user=user).update(accepted_user=None, status=RelationInvite.Status.CREATED, accepted_at=None)
    RelationInvite.objects.filter(creator_user=user).delete()
    user.test_sessions.all().delete(); user.results.all().delete(); user.delete()
