from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from apps.common.api import DocumentedAPIView as APIView
from apps.common.responses import ok
from apps.results.models import ResultSnapshot
from .models import RelationInvite,Relationship
from .services import accept_invite,create_invite,open_invite,serialize_report

class InviteCreateView(APIView):
    def post(self,request):
        invite=create_invite(request.user,get_object_or_404(ResultSnapshot,pk=request.data.get("result_id")))
        return ok({"invite_code":invite.invite_code,"share_path":f"/pages/invite/index?code={invite.invite_code}"},201)
class InviteView(APIView):
    def get(self,request,code):
        invite=open_invite(get_object_or_404(RelationInvite,invite_code=code))
        return ok({"invite_code":invite.invite_code,"status":invite.status,"creator_nickname":invite.creator_user.nickname,"test_slug":invite.creator_result.session.test_version.test.slug})
class InviteAcceptView(APIView):
    def post(self,request,code):
        invite=accept_invite(get_object_or_404(RelationInvite,invite_code=code),request.user)
        return ok({"test_slug":invite.creator_result.session.test_version.test.slug,"invite_id":invite.id})
class RelationshipView(APIView):
    def get(self,request,pk):
        rel=get_object_or_404(Relationship.objects.select_related("report"),pk=pk)
        if request.user.id not in {rel.user_a_id,rel.user_b_id}: raise PermissionDenied("Not a relationship participant")
        return ok(serialize_report(rel.report))
class MyRelationshipsView(APIView):
    def get(self,request):
        from django.db.models import Q
        rows=Relationship.objects.select_related("report").filter(Q(user_a=request.user)|Q(user_b=request.user)).order_by("-created_at")
        return ok([serialize_report(r.report) for r in rows])
