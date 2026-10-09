from rest_framework.permissions import AllowAny
from apps.common.api import DocumentedAPIView as APIView
from apps.common.responses import ok
from .services import delete_user_data, login

class WechatLoginView(APIView):
    permission_classes=[AllowAny]; authentication_classes=[]
    def post(self, request): return ok(login(request.data))

class MeView(APIView):
    def get(self, request): return ok({"id": request.user.id, "nickname": request.user.nickname})

class DeleteMyDataView(APIView):
    def delete(self, request): delete_user_data(request.user); return ok()
