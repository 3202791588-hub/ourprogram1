from typing import Any
from rest_framework.response import Response

def ok(data: Any = None, status: int = 200) -> Response:
    return Response({"code": 0, "message": "ok", "data": {} if data is None else data}, status=status)
