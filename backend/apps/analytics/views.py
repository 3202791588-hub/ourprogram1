from rest_framework.exceptions import ValidationError
from apps.common.api import DocumentedAPIView as APIView
from apps.common.responses import ok
from apps.tests.models import TestSession
from .models import AnalyticsEvent

ALLOWED_EVENTS={"home_view","test_view","test_start","question_answer","test_submit","result_preview","full_result_view","unlock_click","ad_show","ad_complete","ad_error","result_share","invite_create","invite_open","invite_accept","friend_test_complete","relationship_generate","relationship_view","relationship_share"}
class EventView(APIView):
    def post(self,request):
        name=request.data.get("event_name")
        if name not in ALLOWED_EVENTS: raise ValidationError("Unknown event_name")
        session=None
        if request.data.get("session_id"):
            session=TestSession.objects.filter(id=request.data["session_id"],user=request.user).first()
            if session is None: raise ValidationError("Invalid session_id")
        event=AnalyticsEvent.objects.create(user=request.user,session=session,event_name=name,properties=request.data.get("properties",{}))
        return ok({"id":event.id},201)
