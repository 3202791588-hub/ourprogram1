from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from apps.common.api import DocumentedAPIView as APIView
from apps.common.responses import ok
from .models import ResultSnapshot
from .services import serialize_preview, unlock_result

class PreviewView(APIView):
    def get(self,request,pk):
        result=get_object_or_404(ResultSnapshot,pk=pk)
        if result.user_id != request.user.id: raise PermissionDenied("Private preview in Demo")
        return ok(serialize_preview(result))
class FullView(APIView):
    def get(self,request,pk):
        result=get_object_or_404(ResultSnapshot,pk=pk,user=request.user)
        if not result.unlocks.filter(user=request.user).exists(): raise PermissionDenied("Result not unlocked")
        data=serialize_preview(result); data["sections"]=result.result_payload.get("sections",[]); return ok(data)
class UnlockView(APIView):
    def post(self,request,pk):
        result=get_object_or_404(ResultSnapshot,pk=pk)
        unlock=unlock_result(request.user,result,request.data.get("unlock_type","MOCK")); return ok({"unlock_type":unlock.unlock_type})
class MyResultsView(APIView):
    def get(self,request): return ok([serialize_preview(r) for r in ResultSnapshot.objects.filter(user=request.user).order_by("-created_at")])
