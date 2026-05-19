"""Telegram approval service for agent-based message/campaign approvals.

Sends approval requests via Telegram bot with inline buttons.
User clicks approve/reject → webhook updates DB → agent continues.
"""

import os
import json
import logging
import requests
from typing import Dict, Optional, Literal
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


class TelegramApprovalService:
    """Handle approval requests via Telegram bot."""

    @staticmethod
    def send_approval_request(
        approval_id: str,
        title: str,
        preview: str,
        telegram_user_id: int,
        approver_name: str = "",
        context_type: str = "message",  # message, campaign, handoff
        metadata: Dict = None,
    ) -> bool:
        """
        Send approval request via Telegram with inline buttons.

        Args:
            approval_id: Unique ID for this approval request
            title: Title of what needs approval (e.g., "Email M1 - Rajesh Kumar")
            preview: Content preview (first 200 chars of message)
            telegram_user_id: Telegram numeric ID of approver
            approver_name: Name of approver for logging
            context_type: Type of approval (message, campaign, handoff)
            metadata: Additional context to store (campaign_id, prospect_id, etc.)

        Returns:
            bool: True if sent successfully
        """
        if not TELEGRAM_BOT_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN not configured")
            return False

        # Build message
        message_text = f"""
🤖 *Agent Approval Request*

*Type:* {context_type.upper()}
*Item:* {title}

*Preview:*
```
{preview[:300]}
```

👤 *Approver:* {approver_name or "Unknown"}
⏱️ *Sent:* {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

Click below to approve or reject:
"""

        # Inline buttons
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "✅ APPROVE",
                        "callback_data": json.dumps({
                            "action": "approve",
                            "approval_id": approval_id,
                            "type": context_type,
                        }),
                    },
                    {
                        "text": "❌ REJECT",
                        "callback_data": json.dumps({
                            "action": "reject",
                            "approval_id": approval_id,
                            "type": context_type,
                        }),
                    },
                ]
            ]
        }

        # Store approval request in cache (expires in 24 hours)
        cache_key = f"telegram_approval:{approval_id}"
        cache.set(
            cache_key,
            {
                "approval_id": approval_id,
                "title": title,
                "preview": preview,
                "telegram_user_id": telegram_user_id,
                "approver_name": approver_name,
                "context_type": context_type,
                "metadata": metadata or {},
                "sent_at": timezone.now().isoformat(),
                "status": "pending",  # pending, approved, rejected
            },
            86400,  # 24 hours
        )

        # Send via Telegram API
        try:
            response = requests.post(
                f"{TELEGRAM_API_URL}/sendMessage",
                json={
                    "chat_id": telegram_user_id,
                    "text": message_text,
                    "parse_mode": "Markdown",
                    "reply_markup": keyboard,
                },
                timeout=10,
            )

            if response.status_code == 200:
                logger.info(
                    f"Approval request sent to Telegram",
                    extra={
                        "approval_id": approval_id,
                        "telegram_user_id": telegram_user_id,
                        "context_type": context_type,
                    },
                )
                return True
            else:
                logger.error(
                    f"Telegram API error: {response.text}",
                    extra={"approval_id": approval_id},
                )
                return False

        except Exception as e:
            logger.error(f"Failed to send Telegram message: {str(e)}")
            return False

    @staticmethod
    def get_approval_status(approval_id: str) -> Optional[Dict]:
        """
        Check if approval has been completed.

        Returns:
            Dict with status, decision, approver_id, or None if pending
        """
        cache_key = f"telegram_approval:{approval_id}"
        approval_data = cache.get(cache_key)

        if not approval_data:
            logger.warning(f"Approval request not found: {approval_id}")
            return None

        return approval_data

    @staticmethod
    def handle_callback(
        callback_query_id: str,
        telegram_user_id: int,
        action: Literal["approve", "reject"],
        approval_id: str,
        context_type: str,
    ) -> bool:
        """
        Handle button press from Telegram.
        Called by webhook when user clicks approve/reject.

        Args:
            callback_query_id: Telegram callback query ID (to dismiss button)
            telegram_user_id: User who clicked
            action: "approve" or "reject"
            approval_id: Which approval request
            context_type: Type of approval

        Returns:
            bool: True if handled successfully
        """
        if not TELEGRAM_BOT_TOKEN:
            return False

        # Get approval data
        cache_key = f"telegram_approval:{approval_id}"
        approval_data = cache.get(cache_key)

        if not approval_data:
            logger.warning(f"Approval data not found for: {approval_id}")
            return False

        # Verify user
        if approval_data["telegram_user_id"] != telegram_user_id:
            logger.warning(
                f"Unauthorized approval attempt: {telegram_user_id} for {approval_id}"
            )
            return False

        # Mark as completed
        approval_data["status"] = action  # "approved" or "rejected"
        approval_data["decided_at"] = timezone.now().isoformat()
        approval_data["decided_by_telegram_id"] = telegram_user_id
        cache.set(cache_key, approval_data, 86400)

        # Send confirmation to Telegram
        confirmation_text = (
            f"✅ *Approved* by you"
            if action == "approve"
            else f"❌ *Rejected* by you"
        )

        try:
            requests.post(
                f"{TELEGRAM_API_URL}/answerCallbackQuery",
                json={
                    "callback_query_id": callback_query_id,
                    "text": f"{confirmation_text}",
                    "show_alert": False,  # Toast notification, not popup
                },
                timeout=5,
            )

            # Edit original message to show decision
            requests.post(
                f"{TELEGRAM_API_URL}/editMessageReplyMarkup",
                json={
                    "chat_id": telegram_user_id,
                    "message_id": approval_data.get("message_id"),
                    "reply_markup": {
                        "inline_keyboard": [
                            [
                                {
                                    "text": f"{confirmation_text}",
                                    "callback_data": "noop",
                                }
                            ]
                        ]
                    },
                },
                timeout=5,
            )
        except Exception as e:
            logger.error(f"Failed to update Telegram message: {str(e)}")

        logger.info(
            f"Approval {action}: {approval_id}",
            extra={
                "approval_id": approval_id,
                "action": action,
                "telegram_user_id": telegram_user_id,
                "context_type": context_type,
            },
        )

        return True
