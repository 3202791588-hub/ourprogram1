from django.conf import settings
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from apps.tests.models import TestSession
from .engines import get_scoring_engine
from .models import ResultSnapshot, ResultUnlock

@transaction.atomic
def generate_result(session: TestSession) -> ResultSnapshot:
    existing=ResultSnapshot.objects.filter(session=session).first()
    if existing: return existing
    output=get_scoring_engine().calculate(session)
    result=ResultSnapshot.objects.create(user=session.user,session=session,result_type=output.result_type,test_version=session.test_version.version,scoring_version=session.test_version.scoring_version,result_template_version=output.template_version,dimension_scores=output.scores,result_payload=output.payload)
    session.status=TestSession.Status.RESULT_GENERATED; session.save(update_fields=["status","updated_at"])
    if session.relation_invite_id:
        from apps.relations.services import complete_invite
        complete_invite(session.relation_invite,result)
    return result

def serialize_preview(result: ResultSnapshot) -> dict:
    p=result.result_payload
    return {"id":result.id,"result_type":result.result_type,"name":p.get("name"),"tags":p.get("tags",[]),"summary":p.get("summary"),"dimension_scores":result.dimension_scores,"is_unlocked":result.unlocks.filter(user=result.user).exists()}

@transaction.atomic
def unlock_result(user,result: ResultSnapshot,unlock_type: str) -> ResultUnlock:
    if result.user_id != user.id: raise PermissionDenied("Only owner may unlock full result")
    if settings.ADS_ENABLED and unlock_type == ResultUnlock.Type.MOCK: raise ValidationError("Mock unlock disabled when ads are enabled")
    if unlock_type not in ResultUnlock.Type.values: raise ValidationError("Invalid unlock_type")
    unlock,_=ResultUnlock.objects.get_or_create(user=user,result=result,defaults={"unlock_type":unlock_type})
    return unlock
