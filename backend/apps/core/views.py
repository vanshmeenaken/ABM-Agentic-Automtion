"""
Core views for Ken ABM Platform.
"""

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db import connection


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint to verify system is operational.
    Checks database connectivity.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return Response({"status": "healthy", "database": "connected"})
    except Exception as e:
        return Response(
            {"status": "unhealthy", "error": str(e)},
            status=503,
        )
