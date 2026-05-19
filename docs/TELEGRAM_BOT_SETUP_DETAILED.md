# Telegram Bot Setup — Complete Step-by-Step Guide

Follow this guide exactly. It will take ~10 minutes.

---

## STEP 1: Create Your Telegram Bot

### What you need:
- Telegram app (download from App Store, Google Play, or web.telegram.org)

### Do this:

1. **Open Telegram**
   - On phone: Open Telegram app
   - On web: Go to https://web.telegram.org/

2. **Search for @BotFather**
   - Click the search icon (magnifying glass)
   - Type: `@BotFather`
   - Click on "BotFather" (official Telegram bot, has blue checkmark)

3. **Start the bot**
   - Click "Start"
   - You'll see a welcome message from BotFather

4. **Create new bot**
   - Type or click: `/newbot`
   - BotFather asks: "Alright, a new bot. How are we going to call it? Please choose a name for your bot."

5. **Name your bot**
   - Type: `Ken ABM Approval Bot`
   - Press Enter
   - BotFather responds: "Good. Now let's choose a username for your bot..."

6. **Set bot username**
   - Type: `ken_abm_approval_bot`
   - Press Enter
   - BotFather responds with:
     ```
     Done! Congratulations on your new bot. You will find it at t.me/ken_abm_approval_bot.
     You can now add a description, about section and profile picture for your bot, see /help for a list of commands.
     
     Use this token to access the HTTP API:
     123456789:ABCDefGHIjklMNOPQRstuvwxyzABCDefGhi
     
     Keep your token secure and store it safely!
     ```

### ⭐ SAVE THIS TOKEN! 
Example: `123456789:ABCDefGHIjklMNOPQRstuvwxyzABCDefGhi`

This is your **TELEGRAM_BOT_TOKEN**. You'll need it in Step 3.

---

## STEP 2: Get Your Telegram User ID

### What you need:
- Access to @userinfobot (another Telegram bot)

### Do this:

1. **Search for @userinfobot**
   - In Telegram, search for: `@userinfobot`
   - Click on it (has blue checkmark)

2. **Start the bot**
   - Click "Start"

3. **Get your ID**
   - Type any message (e.g., "hi")
   - Press Enter
   - Bot responds with something like:
     ```
     User ID: 987654321
     First Name: Vansh
     ...
     ```

### ⭐ SAVE THIS NUMBER!
This is your **TELEGRAM_USER_ID** (or **TELEGRAM_APPROVER_ID**). Example: `987654321`

You now have:
- ✅ TELEGRAM_BOT_TOKEN: `123456789:ABCDefGHIjklMNOPQRstuvwxyzABCDefGhi`
- ✅ TELEGRAM_USER_ID: `987654321`

---

## STEP 3: Configure Django

### What you need:
- Text editor (VS Code, Notepad, etc.)
- Access to your project files

### Do this:

1. **Open `.env` file**
   - Location: `c:\Users\Vansh\ken-abm-platform\.env`
   - If it doesn't exist, create it in the root folder

2. **Add these two lines:**
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCDefGHIjklMNOPQRstuvwxyzABCDefGhi
   TELEGRAM_USER_ID=987654321
   ```
   
   Replace:
   - `123456789:ABCDefGHIjklMNOPQRstuvwxyzABCDefGhi` with YOUR token from Step 1
   - `987654321` with YOUR user ID from Step 2

3. **Save the file**
   - Ctrl+S (Windows) or Cmd+S (Mac)

✅ Django will automatically read these environment variables.

---

## STEP 4: Set Up Telegram Webhook (Production Only)

### ⚠️ Important: Only do this if your backend is already deployed!

If you're still in **local development** (running on localhost), skip this step.

### If deployed to production:

1. **Get your backend URL**
   - Example: `https://api.yourcompany.com` or `https://your-railway-app.up.railway.app`

2. **Open Terminal/Command Prompt**

3. **Run this command** (replace `YOUR_TOKEN` with your actual token):
   ```bash
   curl https://api.telegram.org/botYOUR_TOKEN/setWebhook \
     -F url=https://api.yourcompany.com/api/v1/webhooks/telegram/
   ```

   Example:
   ```bash
   curl https://api.telegram.org/bot123456789:ABCDefGHIjklMNOPQRstuvwxyzABCDefGhi/setWebhook \
     -F url=https://api.yourcompany.com/api/v1/webhooks/telegram/
   ```

4. **You should see response:**
   ```json
   {"ok": true, "result": true, "description": "Webhook was set"}
   ```

5. **Verify webhook is set:**
   ```bash
   curl https://api.telegram.org/botYOUR_TOKEN/getWebhookInfo
   ```

✅ Telegram bot is now connected to your backend!

---

## STEP 5: Test the Bot (Local Development)

### Run this in Django shell:

1. **Open Terminal/Command Prompt**

2. **Navigate to backend folder:**
   ```bash
   cd c:\Users\Vansh\ken-abm-platform\backend
   ```

3. **Start Django shell:**
   ```bash
   python manage.py shell
   ```

4. **Run this code:**
   ```python
   from apps.core.telegram_service import TelegramApprovalService
   from django.conf import settings

   # Send test message
   success = TelegramApprovalService.send_approval_request(
       approval_id="test_001",
       title="Test Email M1 - Rajesh Kumar",
       preview="Hi Rajesh, we recently finished a mandate on Crop Protection Pesticides. While reviewing the findings, we discovered something most leaders at your level aren't tracking yet...",
       telegram_user_id=int(settings.TELEGRAM_APPROVER_ID),
       approver_name="Vansh",
       context_type="message"
   )

   print(f"Message sent: {success}")
   ```

5. **Check your Telegram**
   - You should see a message from @ken_abm_approval_bot with:
     - Title: "Test Email M1 - Rajesh Kumar"
     - Message preview
     - Two buttons: ✅ APPROVE | ❌ REJECT

6. **Click APPROVE button**
   - Button should show confirmation
   - Message should show ✅ Approved by you

7. **Back in Django shell, check status:**
   ```python
   status = TelegramApprovalService.get_approval_status("test_001")
   print(status)
   ```

   You should see:
   ```
   {
       'approval_id': 'test_001',
       'status': 'approved',
       'decided_at': '2026-05-19T14:30:00',
       ...
   }
   ```

8. **Exit Django shell:**
   ```
   exit()
   ```

✅ Telegram bot is working!

---

## STEP 6: How Agents Will Use This

### When Compliance Review Agent runs:

1. **Agent checks message for compliance violations**
   - If violations found → BLOCKED (cannot be approved)
   - If passes → sends to Telegram

2. **You receive Telegram notification**
   - Message with preview of the content
   - Two buttons: ✅ APPROVE | ❌ REJECT

3. **You click button**
   - ✅ APPROVE → message approved, ready to send
   - ❌ REJECT → agent regenerates message or notifies creator

4. **Agent continues automatically**
   - Checks Telegram approval status
   - If approved → sends message to prospect
   - If rejected → logs rejection, stops workflow

---

## STEP 7: Troubleshooting

### Problem: "TELEGRAM_BOT_TOKEN not configured"

**Solution:**
- Check `.env` file has correct token (no extra spaces)
- Make sure file is saved
- Restart Django server if running

### Problem: "Telegram API error" in logs

**Solution:**
- Verify token is correct (copy from BotFather again)
- Make sure user ID is numeric (no quotes)
- Check internet connection

### Problem: Message not arriving in Telegram

**Solution:**
- In Telegram, message the bot first: `@ken_abm_approval_bot`
- Click "Start"
- Then try test again
- If still no message, check Django logs for errors

### Problem: Button click not working

**Solution:**
- Only works if webhook is set up (Step 4)
- For local development, use polling pattern (agent checks status repeatedly)

---

## STEP 8: Environment Variables Summary

Your `.env` should now have:

```
# Telegram approval bot
TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
TELEGRAM_USER_ID=YOUR_USER_ID_HERE

# Other existing variables...
DJANGO_SECRET_KEY=...
DEBUG=True
...
```

---

## STEP 9: What's Next?

Once this is working:

1. **Build Compliance Review Agent** that uses this Telegram approval
2. **Build Message model** with approval status field
3. **Integrate with copy agents** (Email, LinkedIn, WhatsApp)
4. **Full workflow:** Agent generates → Telegram approval → Send message

---

## Quick Reference

| Item | Where to get |
|------|-------------|
| TELEGRAM_BOT_TOKEN | BotFather `/newbot` response |
| TELEGRAM_USER_ID | @userinfobot response |
| Webhook URL | Your deployed backend URL |
| Django config | In `.env` file |
| Test endpoint | `POST /api/v1/webhooks/telegram/` |

---

## Questions?

If anything is unclear:
1. Check the logs: `python manage.py shell` → any error messages?
2. Verify token in BotFather again
3. Make sure bot received `/start` command first
4. Check firewall/network isn't blocking Telegram API calls

You're all set! 🎉

