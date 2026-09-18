from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(
            {
                "status": "success",
                "message": "ToolShare API is running",
            },
            status=status.HTTP_200_OK,
        )