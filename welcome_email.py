"""
welcome_email.py - Send welcome email to new users after signup.
Uses the existing Gmail integration via gmail_client.
"""

import logging
import threading
from gmail_client import send_email

logger = logging.getLogger("voicemail_app")


def _build_welcome_html(user_name, user_email):
    name = user_name or "there"
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f4f4f7;font-family:'Helvetica Neue',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f7;padding:40px 20px;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

<tr><td style="background:linear-gradient(135deg,#1a73e8 0%,#4285f4 100%);padding:40px;text-align:center;">
  <h1 style="margin:0;color:#ffffff;font-size:28px;font-weight:800;">Welcome to Open Human!</h1>
  <p style="margin:12px 0 0;color:rgba(255,255,255,0.85);font-size:15px;">Your account has been created successfully</p>
</td></tr>

<tr><td style="padding:40px;">
  <p style="font-size:16px;color:#333;line-height:1.6;margin:0 0 20px;">Hi {name},</p>
  <p style="font-size:15px;color:#555;line-height:1.7;margin:0 0 20px;">Thank you for signing up for <strong>Open Human</strong> - your intelligent communication platform for outbound voicemail campaigns.</p>

  <div style="background:#f0f7ff;border:1px solid #d0e3ff;border-radius:10px;padding:24px;margin:24px 0;">
    <h3 style="margin:0 0 12px;color:#1a73e8;font-size:16px;">What you can do:</h3>
    <ul style="margin:0;padding:0 0 0 20px;color:#555;font-size:14px;line-height:2;">
      <li>Upload phone lists and launch outbound campaigns</li>
      <li>Auto-detect answering machines and drop voicemails</li>
      <li>Transfer human-answered calls to your team</li>
      <li>Create personalized voicemails with AI voices</li>
      <li>Track results with detailed analytics and reports</li>
    </ul>
  </div>

  <p style="font-size:15px;color:#555;line-height:1.7;margin:0 0 24px;">Get started by setting up your profile and creating your first campaign.</p>

  <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
    <tr><td style="background:#1a73e8;border-radius:8px;">
      <a href="#" style="display:inline-block;padding:14px 32px;color:#fff;text-decoration:none;font-size:15px;font-weight:600;">Go to Dashboard</a>
    </td></tr>
  </table>
</td></tr>

<tr><td style="padding:24px 40px;background:#f8f9fa;border-top:1px solid #e8e8e8;text-align:center;">
  <p style="margin:0;font-size:12px;color:#999;">Need help? Just reply to this email and we'll get back to you.</p>
  <p style="margin:8px 0 0;font-size:11px;color:#bbb;">Open Human - Intelligent Communication at Scale</p>
</td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""


def send_welcome_email(user_email, user_name=None):
    try:
        html_body = _build_welcome_html(user_name, user_email)
        text_body = f"""Welcome to Open Human!

Hi {user_name or 'there'},

Thank you for signing up for Open Human - your intelligent communication platform.

Your account has been created and you're ready to start creating campaigns.

Need help? Just reply to this email.

- Open Human Team"""

        success = send_email(
            to_email=user_email,
            subject="Welcome to Open Human! 🚀",
            html_body=html_body,
            text_body=text_body,
        )
        if success:
            logger.info(f"Welcome email sent to {user_email}")
        else:
            logger.warning(f"Failed to send welcome email to {user_email}")
        return success
    except Exception as e:
        logger.error(f"Error sending welcome email to {user_email}: {e}")
        return False


def send_welcome_email_async(user_email, user_name=None):
    thread = threading.Thread(
        target=send_welcome_email,
        args=(user_email, user_name),
        daemon=True,
    )
    thread.start()
