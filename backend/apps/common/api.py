from rest_framework import serializers
from rest_framework.views import APIView

class EmptySerializer(serializers.Serializer):
    pass

class DocumentedAPIView(APIView):
    """APIView base that keeps every endpoint visible in generated OpenAPI."""
    serializer_class = EmptySerializer
