from rest_framework.permissions import AllowAny
from .api import DocumentedAPIView as APIView
from .responses import ok

class HealthView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request):
        return ok({"status": "ok"})
