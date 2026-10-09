import secrets
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied,ValidationError
from .engines import get_relation_engine
from .models import RelationInvite,Relationship,RelationshipReport

@transaction.atomic
def create_invite(user,result)->RelationInvite:
    if result.user_id!=user.id: raise PermissionDenied("Cannot invite from another user's result")
    invite=RelationInvite.objects.filter(creator_result=result,status__in=[RelationInvite.Status.CREATED,RelationInvite.Status.OPENED]).first()
    return invite or RelationInvite.objects.create(creator_user=user,creator_result=result,invite_code=secrets.token_urlsafe(32))

@transaction.atomic
def open_invite(invite:RelationInvite)->RelationInvite:
    if invite.expires_at and invite.expires_at<=timezone.now(): invite.status=RelationInvite.Status.EXPIRED; invite.save(update_fields=["status"])
    elif invite.status==RelationInvite.Status.CREATED: invite.status=RelationInvite.Status.OPENED; invite.save(update_fields=["status"])
    return invite

@transaction.atomic
def accept_invite(invite:RelationInvite,user)->RelationInvite:
    invite=RelationInvite.objects.select_for_update().get(pk=invite.pk)
    if invite.creator_user_id==user.id: raise ValidationError("Cannot accept your own invite")
    if invite.status==RelationInvite.Status.EXPIRED: raise ValidationError("Invite expired")
    if invite.accepted_user_id and invite.accepted_user_id!=user.id: raise ValidationError("Invite already accepted")
    if invite.status==RelationInvite.Status.COMPLETED and invite.accepted_user_id==user.id: return invite
    invite.accepted_user=user; invite.status=RelationInvite.Status.ACCEPTED; invite.accepted_at=invite.accepted_at or timezone.now(); invite.save(update_fields=["accepted_user","status","accepted_at"])
    return invite

@transaction.atomic
def complete_invite(invite:RelationInvite,result_b)->RelationshipReport:
    invite=RelationInvite.objects.select_for_update().get(pk=invite.pk)
    if invite.accepted_user_id!=result_b.user_id: raise PermissionDenied("Result owner is not invite acceptor")
    existing=RelationshipReport.objects.filter(relationship__invite=invite).first()
    if existing: return existing
    output=get_relation_engine().calculate(invite.creator_result,result_b)
    relationship=Relationship.objects.create(user_a=invite.creator_user,user_b=result_b.user,result_a=invite.creator_result,result_b=result_b,invite=invite,relation_algorithm_version=output.version)
    report=RelationshipReport.objects.create(relationship=relationship,relation_type=output.relation_type,compatibility_score=output.score,dimension_scores=output.scores,report_payload=output.payload,relation_algorithm_version=output.version)
    invite.status=RelationInvite.Status.COMPLETED; invite.save(update_fields=["status"])
    return report

def serialize_report(report:RelationshipReport)->dict:
    return {"id":report.relationship_id,"relation_type":report.relation_type,"compatibility_score":report.compatibility_score,"dimension_scores":report.dimension_scores,"report_payload":report.report_payload,"user_a_id":report.relationship.user_a_id,"user_b_id":report.relationship.user_b_id}
