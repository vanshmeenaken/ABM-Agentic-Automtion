"""Telegram webhook handler for approval button callbacks."""

import json
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .telegram_service import TelegramApprovalService

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def telegram_callback_webhook(request):
    """
    Webhook endpoint: POST /api/v1/webhooks/telegram/

    Telegram sends callback_query when user clicks approve/reject button.

    Payload:
    {
        "update_id": 123456789,
        "callback_query": {
            "id": "callback_id",
            "from": {"id": 987654321, "first_name": "Name"},
            "message": {"message_id": 42, ...},
            "data": "{\"action\": \"approve\", \"approval_id\": \"msg_123\", \"type\": \"message\"}"
        }
    }
    """
    try:
        body = json.loads(request.body)
        logger.info(f"Telegram webhook received: {body}")

        # Extract callback query
        callback_query = body.get("callback_query")
        if not callback_query:
            logger.warning("No callback_query in request")
            return JsonResponse({"ok": True})  # Still return 200 to Telegram

        # Parse button data
        callback_data_str = callback_query.get("data", "{}")
        try:
            callback_data = json.loads(callback_data_str)
        except json.JSONDecodeError:
            logger.error(f"Invalid callback data: {callback_data_str}")
            return JsonResponse({"ok": True})

        # Extract info
        action = callback_data.get("action")  # approve or reject
        approval_id = callback_data.get("approval_id")
        context_type = callback_data.get("type", "message")
        callback_query_id = callback_query.get("id")
        telegram_user_id = callback_query.get("from", {}).get("id")

        if not all([action, approval_id, callback_query_id, telegram_user_id]):
            logger.error(f"Missing required fields in callback_data: {callback_data}")
            return JsonResponse({"ok": True})

        # Handle approval decision
        success = TelegramApprovalService.handle_callback(
            callback_query_id=callback_query_id,
            telegram_user_id=telegram_user_id,
            action=action,
            approval_id=approval_id,
            context_type=context_type,
        )

        if success:
            return JsonResponse(
                {"ok": True, "action": action, "approval_id": approval_id}
            )
        else:
            return JsonResponse(
                {"ok": False, "error": "Failed to process approval"},
                status=400,
            )

    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        return JsonResponse({"ok": True})
    except Exception as e:
        logger.error(f"Unexpected error in telegram_callback_webhook: {str(e)}")
        return JsonResponse({"ok": True})  # Always return 200 to Telegram to prevent retries
