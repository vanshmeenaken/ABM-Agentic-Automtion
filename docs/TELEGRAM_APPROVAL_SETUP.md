# Telegram Approval Bot Setup

Real-time agent approval via Telegram. Agents send approval requests → you click button → agent continues.

---

## 1. Create Telegram Bot

1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Name it: `Ken ABM Approval Bot` (or your preferred name)
4. Username: `ken_abm_approval_bot` (or similar)
5. You'll get a **TOKEN** like: `123456789:ABCDefGHIjklMNOPQRstuvwxyzABCDefGhi`
6. Save this token

---

## 2. Get Your Telegram User ID

1. Open Telegram, search for `@userinfobot`
2. Send any message
3. Bot replies with your **User ID** (numeric, like `987654321`)
4. Save this ID

---

## 3. Configure Django

Add to `.env`:
```
TELEGRAM_BOT_TOKEN=123456789:ABCDefGHIjklMNOPQRstuvwxyzABCDefGhi
TELEGRAM_USER_ID=987654321
```

Add to `backend/config/settings/base.py`:
```python
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_APPROVER_ID = int(os.getenv("TELEGRAM_USER_ID", 0))
```

---

## 4. Setup Telegram Webhook

Point Telegram bot to your webhook endpoint:

```bash
curl https://api.telegram.org/bot{YOUR_TOKEN}/setWebhook \
  -F url=https://your-domain.com/api/v1/webhooks/telegram/
```

Test:
```bash
curl https://api.telegram.org/bot{YOUR_TOKEN}/getWebhookInfo
```

---

## 5. How Agents Use This

### Send Approval Request

```python
from apps.core.telegram_service import TelegramApprovalService
from django.conf import settings

# In your agent (e.g., Compliance Review Agent)
success = TelegramApprovalService.send_approval_request(
    approval_id="msg_12345",
    title="Email M1 - Rajesh Kumar, Syngenta India",
    preview="Hi Rajesh, we recently finished a mandate on Crop Protection Pesticides...",
    telegram_user_id=settings.TELEGRAM_APPROVER_ID,
    approver_name="Vansh",
    context_type="message",  # or "campaign", "handoff"
    metadata={
        "campaign_id": "campaign_123",
        "prospect_id": "prospect_456",
        "message_stage": "M1"
    }
)

if not success:
    # Handle error - maybe fallback to email approval
    log_event("Telegram approval failed, fallback to manual queue")
```

### Wait for Response (Polling)

```python
import time
from apps.core.telegram_service import TelegramApprovalService

# Agent waits for approval (max 24 hours, cached)
timeout = 1440  # 24 hours in minutes
start_time = time.time()

while True:
    approval_status = TelegramApprovalService.get_approval_status("msg_12345")
    
    if approval_status["status"] == "approved":
        # Continue with message send
        send_message_sequence()
        break
    elif approval_status["status"] == "rejected":
        # Log rejection, notify creator
        log_event("Message rejected by approver")
        break
    
    # Check timeout
    elapsed = (time.time() - start_time) / 60
    if elapsed > timeout:
        # Approval expired, mark as unapproved
        log_event("Approval timeout - message not sent")
        break
    
    time.sleep(30)  # Check every 30 seconds
```

### Async Pattern (Celery Task)

```python
from celery import shared_task
from apps.core.telegram_service import TelegramApprovalService

@shared_task
def wait_for_approval_async(approval_id):
    """
    Celery task that waits for Telegram approval.
    Called after agent sends approval request.
    """
    max_retries = 2880  # 24 hours * 60 / 30 seconds per check
    retry_count = 0
    
    while retry_count < max_retries:
        approval_status = TelegramApprovalService.get_approval_status(approval_id)
        
        if approval_status["status"] == "approved":
            # Trigger next step (e.g., send message)
            from apps.messages.tasks import send_message_task
            send_message_task.delay(approval_id)
            return {"status": "approved"}
        
        elif approval_status["status"] == "rejected":
            return {"status": "rejected"}
        
        # Still pending, retry in 30 seconds
        retry_count += 1
        return wait_for_approval_async.apply_async(
            args=[approval_id],
            countdown=30
        )
    
    # Timeout
    return {"status": "timeout"}
```

---

## 6. Full Workflow Example: Compliance Review Agent

```python
# agents/compliance_review_agent.py

from apps.core.telegram_service import TelegramApprovalService
from django.conf import settings

def run_compliance_review_agent(message_id, message_body):
    """
    1. Check message for compliance issues
    2. If PASS → send approval request via Telegram
    3. Wait for user decision
    4. Update DB with approval status
    """
    
    # Step 1: Check compliance
    compliance_result = check_compliance(message_body)
    
    if compliance_result["has_violations"]:
        # Block - cannot be approved
        return {
            "status": "blocked",
            "violations": compliance_result["violations"],
            "action": "regenerate"
        }
    
    # Step 2: Compliance passed - request human approval
    preview = message_body[:250] + "..." if len(message_body) > 250 else message_body
    
    success = TelegramApprovalService.send_approval_request(
        approval_id=f"msg_{message_id}",
        title=f"Compliance Check Passed - {message_id}",
        preview=preview,
        telegram_user_id=settings.TELEGRAM_APPROVER_ID,
        approver_name="Content Approver",
        context_type="message",
        metadata={"message_id": message_id}
    )
    
    if not success:
        return {"status": "error", "reason": "Failed to send Telegram notification"}
    
    # Step 3: Wait for approval (async via Celery)
    from celery import shared_task
    
    @shared_task
    def wait_and_update(msg_id):
        max_attempts = 2880
        attempt = 0
        
        while attempt < max_attempts:
            approval_data = TelegramApprovalService.get_approval_status(f"msg_{msg_id}")
            
            if approval_data["status"] == "approved":
                # Update message record
                update_message_approval_status(msg_id, "approved")
                return {"status": "approved"}
            
            elif approval_data["status"] == "rejected":
                # Log rejection
                update_message_approval_status(msg_id, "rejected")
                notify_creator(msg_id, "rejected")
                return {"status": "rejected"}
            
            attempt += 1
            time.sleep(30)
        
        # Timeout
        return {"status": "timeout"}
    
    # Trigger async wait
    wait_and_update.delay(message_id)
    
    return {"status": "pending", "approval_id": f"msg_{message_id}"}
```

---

## 7. Message Approval States

```
Message created by agent
    ↓
Compliance check (compliance_review_agent runs)
    ↓
    ├─ BLOCKED (violations found) → cannot be approved
    └─ PASSED → send to Telegram
        ↓
        Telegram approval request sent
        ↓
        ├─ APPROVED (you click ✅) → message ready to send
        └─ REJECTED (you click ❌) → return to agent for regeneration
```

---

## 8. Testing

### Test Telegram API

```bash
# Get bot info
curl https://api.telegram.org/bot{TOKEN}/getMe

# Get webhook status
curl https://api.telegram.org/bot{TOKEN}/getWebhookInfo

# Send test message
curl https://api.telegram.org/bot{TOKEN}/sendMessage \
  -d "chat_id={YOUR_USER_ID}&text=Test+message"
```

### Test Approval Flow (Django shell)

```python
from apps.core.telegram_service import TelegramApprovalService
from django.conf import settings

# Send approval request
success = TelegramApprovalService.send_approval_request(
    approval_id="test_001",
    title="Test Email M1",
    preview="Hi there, this is a test message preview.",
    telegram_user_id=settings.TELEGRAM_APPROVER_ID,
    approver_name="Test User"
)
print(f"Sent: {success}")

# Check status
status = TelegramApprovalService.get_approval_status("test_001")
print(f"Status: {status}")

# After you approve in Telegram, check again
status = TelegramApprovalService.get_approval_status("test_001")
print(f"Status after approval: {status}")
```

---

## 9. Production Checklist

- [ ] Telegram bot token in `.env` (not hardcoded)
- [ ] Webhook URL points to production domain
- [ ] SSL certificate valid on webhook endpoint
- [ ] Rate limiting configured (Telegram sends multiple retries)
- [ ] Error handling for timeout (24-hour cache expiry)
- [ ] Fallback to manual queue if Telegram fails
- [ ] Audit log captures approver decision + timestamp
- [ ] Alert if approval takes > 4 hours (may be missed)

---

## 10. Future Extensions

- Multi-approver (route based on approval type)
- Rejection reason input (when user clicks reject)
- Scheduled approval reminder (if pending > 2 hours)
- Campaign approval via Telegram
- Handoff approval via Telegram
- Slack integration (same pattern)

