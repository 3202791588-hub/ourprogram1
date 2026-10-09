from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from apps.common.api import DocumentedAPIView as APIView
from apps.common.responses import ok
from apps.results.models import ResultSnapshot
from .models import AdEvent

class AdEventView(APIView):
    def post(self,request):
        result=get_object_or_404(ResultSnapshot,pk=request.data.get("result_id"))
        if result.user_id!=request.user.id: raise PermissionDenied("Cannot record ad for another user")
        event=request.data.get("event")
        if event not in AdEvent.Event.values: raise PermissionDenied("Invalid ad event")
        row=AdEvent.objects.create(user=request.user,result=result,event=event,metadata=request.data.get("metadata",{}))
        return ok({"id":row.id},201)
