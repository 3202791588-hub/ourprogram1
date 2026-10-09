from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError
from apps.relations.models import RelationInvite
from .models import Answer, Question, QuestionOption, Test, TestSession, TestVersion

@transaction.atomic
def create_session(user, test_slug: str, relation_invite_id: int | None = None) -> TestSession:
    test=get_object_or_404(Test,slug=test_slug,status=Test.Status.PUBLISHED)
    version=test.versions.filter(status=TestVersion.Status.PUBLISHED).order_by("-version").first()
    if version is None: raise ValidationError("No published test version")
    invite=None
    if relation_invite_id:
        invite=get_object_or_404(RelationInvite,id=relation_invite_id)
        if invite.accepted_user_id != user.id or invite.status not in {RelationInvite.Status.ACCEPTED,RelationInvite.Status.COMPLETED}: raise PermissionDenied("Invite not accepted by this user")
        version=invite.creator_result.session.test_version
        if version.test_id != test.id: raise ValidationError("Invite belongs to a different test")
    existing=TestSession.objects.filter(user=user,test_version=version,relation_invite=invite,status__in=[TestSession.Status.CREATED,TestSession.Status.ANSWERING]).first()
    return existing or TestSession.objects.create(user=user,test_version=version,relation_invite=invite)

@transaction.atomic
def save_answer(session: TestSession, question_id: int, option_id: int) -> Answer:
    if session.status in {TestSession.Status.SUBMITTED,TestSession.Status.RESULT_GENERATED}: raise ValidationError("Session already submitted")
    question=get_object_or_404(Question,id=question_id,test_version=session.test_version)
    option=get_object_or_404(QuestionOption,id=option_id,question=question)
    answer,_=Answer.objects.update_or_create(session=session,question=question,defaults={"option":option})
    session.status=TestSession.Status.ANSWERING; session.current_question=min(question.sequence+1,session.test_version.question_count); session.save(update_fields=["status","current_question","updated_at"])
    return answer

@transaction.atomic
def submit_session(session: TestSession):
    from apps.results.services import generate_result
    locked=TestSession.objects.select_for_update().get(pk=session.pk)
    if hasattr(locked,"result"):
        return locked.result
    answered=locked.answers.values("question_id").distinct().count()
    if answered != locked.test_version.question_count: raise ValidationError({"answers":f"Expected {locked.test_version.question_count}, got {answered}"})
    locked.status=TestSession.Status.SUBMITTED; locked.submitted_at=timezone.now(); locked.save(update_fields=["status","submitted_at","updated_at"])
    return generate_result(locked)
