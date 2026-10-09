from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import PermissionDenied
from apps.common.api import DocumentedAPIView as APIView
from apps.common.responses import ok
from .models import Test, TestSession
from .serializers import CreateSessionSerializer, SaveAnswerSerializer, SessionSerializer, TestDetailSerializer, TestListSerializer
from .services import create_session, save_answer, submit_session

class TestListView(APIView):
    @extend_schema(operation_id="list_tests", responses=TestListSerializer(many=True))
    def get(self,request): return ok(TestListSerializer(Test.objects.filter(status=Test.Status.PUBLISHED),many=True).data)
class TestDetailView(APIView):
    @extend_schema(operation_id="retrieve_test", responses=TestDetailSerializer)
    def get(self,request,slug): return ok(TestDetailSerializer(get_object_or_404(Test,slug=slug,status=Test.Status.PUBLISHED)).data)
class SessionListView(APIView):
    def post(self,request):
        s=CreateSessionSerializer(data=request.data); s.is_valid(raise_exception=True)
        obj=create_session(request.user,**s.validated_data); return ok(SessionSerializer(obj).data,201)
class SessionView(APIView):
    def get_obj(self,request,pk): return get_object_or_404(TestSession.objects.select_related("test_version").prefetch_related("answers","test_version__questions__options"),pk=pk,user=request.user)
    def get(self,request,pk): return ok(SessionSerializer(self.get_obj(request,pk)).data)
class AnswerView(SessionView):
    def put(self,request,pk):
        session=self.get_obj(request,pk); s=SaveAnswerSerializer(data=request.data); s.is_valid(raise_exception=True)
        answer=save_answer(session,**s.validated_data); return ok({"question_id":answer.question_id,"option_id":answer.option_id})
class SubmitView(SessionView):
    def post(self,request,pk):
        result=submit_session(self.get_obj(request,pk))
        relationship=getattr(getattr(result.session,"relation_invite",None),"relationship",None)
        return ok({"result_id":result.id,"relationship_id":relationship.id if relationship else None})
