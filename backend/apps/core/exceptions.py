"""
Custom API exceptions for Ken ABM Platform.
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class AgentFailureException(APIException):
    """Raised when an AI agent fails to complete its task."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "AI agent failed to process request."
    default_code = "agent_failure"


class CampaignStateTransitionException(APIException):
    """Raised when an invalid campaign state transition is attempted."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid campaign state transition."
    default_code = "invalid_state_transition"


class InsufficientPermissionsException(APIException):
    """Raised when user lacks required permissions."""

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Insufficient permissions for this action."
    default_code = "insufficient_permissions"


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF to provide consistent error responses.
    """
    from rest_framework.views import exception_handler

    response = exception_handler(exc, context)

    if response is not None:
        response.data["type"] = exc.__class__.__name__
        if hasattr(exc, "detail"):
            response.data["detail"] = str(exc.detail)

    return response
