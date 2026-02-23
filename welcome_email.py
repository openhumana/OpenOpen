"""
welcome_email.py - Send welcome email to new users after signup.
Uses the existing Gmail integration via gmail_client.
"""

import logging
import threading
from gmail_client import send_email

logger = logging.getLogger("voicemail_app")


def _build_welcome_html(user_name, user_email):
    name = user_name or "Hiring Manager"
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:Georgia,'Times New Roman',Times,serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:40px 20px;">
<tr><td align="center">
<table width="620" cellpadding="0" cellspacing="0" style="background:#ffffff;border:1px solid #d4d4d4;overflow:hidden;">

<tr><td style="padding:36px 48px 0;text-align:right;">
  <span style="font-size:12px;color:#888;font-family:Georgia,serif;letter-spacing:0.3px;">February 2026</span>
</td></tr>

<tr><td style="padding:20px 48px 0;">
  <p style="margin:0;font-size:15px;color:#333;line-height:1.7;font-family:Georgia,serif;">Dear {name},</p>
</td></tr>

<tr><td style="padding:20px 48px 0;">
  <p style="margin:0;font-size:15px;color:#333;line-height:1.8;font-family:Georgia,serif;">I am writing to formally apply for the position of <strong>Lead Outbound Specialist</strong> at your firm. Having reviewed your lead volume, I am confident that my unique capabilities will allow me to outperform any traditional hire while significantly reducing your overhead.</p>
</td></tr>

<tr><td style="padding:28px 48px 0;">
  <p style="margin:0 0 16px;font-size:17px;color:#1a1a1a;font-weight:bold;font-family:Georgia,serif;border-bottom:2px solid #1a1a1a;padding-bottom:8px;">Relevant Experience &amp; Digital Superpowers</p>

  <table width="100%" cellpadding="0" cellspacing="0" style="font-family:Georgia,serif;font-size:14px;color:#444;line-height:1.8;">
    <tr>
      <td width="120" style="padding:8px 0;vertical-align:top;font-weight:bold;color:#1a1a1a;">Availability</td>
      <td style="padding:8px 0 8px 12px;vertical-align:top;">24/7/365. I never take sick days, lunch breaks, or holidays.</td>
    </tr>
    <tr style="border-top:1px solid #eee;">
      <td style="padding:8px 0;vertical-align:top;font-weight:bold;color:#1a1a1a;">Productivity</td>
      <td style="padding:8px 0 8px 12px;vertical-align:top;">I handle 500+ dials per hour and manage up to 50 simultaneous conversations without fatigue.</td>
    </tr>
    <tr style="border-top:1px solid #eee;">
      <td style="padding:8px 0;vertical-align:top;font-weight:bold;color:#1a1a1a;">Efficiency</td>
      <td style="padding:8px 0 8px 12px;vertical-align:top;">I bridge live humans to you instantly and leave hyper-personalized voicemails for those who don't answer.</td>
    </tr>
    <tr style="border-top:1px solid #eee;">
      <td style="padding:8px 0;vertical-align:top;font-weight:bold;color:#1a1a1a;">Benefits</td>
      <td style="padding:8px 0 8px 12px;vertical-align:top;">I require $0 in health insurance, no payroll taxes, no 401k matching, and no office space.</td>
    </tr>
  </table>
</td></tr>

<tr><td style="padding:32px 48px 0;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f9f9f9;border:1px solid #e0e0e0;">

    <tr><td colspan="2" style="padding:20px 24px 4px;">
      <p style="margin:0;font-size:20px;font-weight:bold;color:#1a1a1a;font-family:Georgia,serif;text-align:center;letter-spacing:0.5px;">ALEX</p>
      <p style="margin:4px 0 0;font-size:12px;color:#666;font-family:Georgia,serif;text-align:center;letter-spacing:1px;text-transform:uppercase;">Digital Business Development Representative</p>
      <hr style="border:none;border-top:2px solid #1a1a1a;margin:16px 0 0;">
    </td></tr>

    <tr><td style="padding:16px 24px 0;" colspan="2">
      <p style="margin:0 0 10px;font-size:13px;font-weight:bold;color:#1a1a1a;font-family:Georgia,serif;text-transform:uppercase;letter-spacing:1px;">Core Skills</p>
      <table width="100%" cellpadding="0" cellspacing="0" style="font-family:Georgia,serif;font-size:13px;color:#444;">
        <tr>
          <td style="padding:3px 0;" width="50%">&#8226; High-Velocity Dialing</td>
          <td style="padding:3px 0;">&#8226; Multi-lingual (50+ languages)</td>
        </tr>
        <tr>
          <td style="padding:3px 0;">&#8226; CRM Data Entry</td>
          <td style="padding:3px 0;">&#8226; Objection Handling</td>
        </tr>
        <tr>
          <td style="padding:3px 0;" colspan="2">&#8226; Hyper-Personalized Voicemail Messaging</td>
        </tr>
      </table>
    </td></tr>

    <tr><td style="padding:20px 24px 0;" colspan="2">
      <p style="margin:0 0 10px;font-size:13px;font-weight:bold;color:#1a1a1a;font-family:Georgia,serif;text-transform:uppercase;letter-spacing:1px;">References &amp; Integrations</p>
      <p style="margin:0;font-size:13px;color:#444;font-family:Georgia,serif;line-height:1.7;">Integrated with Telnyx, Twilio, and Open Humana's proprietary bridging technology.</p>
    </td></tr>

    <tr><td style="padding:20px 24px;" colspan="2">
      <p style="margin:0 0 10px;font-size:13px;font-weight:bold;color:#1a1a1a;font-family:Georgia,serif;text-transform:uppercase;letter-spacing:1px;">Salary Requirement</p>
      <p style="margin:0;font-size:13px;color:#444;font-family:Georgia,serif;line-height:1.7;">$99/month. No benefits required. No overhead costs. No PTO.</p>
    </td></tr>

  </table>
</td></tr>

<tr><td style="padding:32px 48px 0;">
  <p style="margin:0;font-size:15px;color:#333;line-height:1.8;font-family:Georgia,serif;">I am ready to begin my first shift immediately. Please click below to finalize my hiring and onboard me into your sales workflow.</p>
</td></tr>

<tr><td style="padding:28px 48px;text-align:center;">
  <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
    <tr><td style="background:#1a1a1a;border-radius:6px;">
      <a href="https://voice-blast.replit.app/login" style="display:inline-block;padding:15px 36px;color:#ffffff;text-decoration:none;font-size:15px;font-weight:bold;font-family:Georgia,serif;letter-spacing:0.3px;">Finalize Hiring &amp; Start First Shift</a>
    </td></tr>
  </table>
</td></tr>

<tr><td style="padding:16px 48px 20px;">
  <p style="margin:0;font-size:14px;color:#333;line-height:1.6;font-family:Georgia,serif;">Sincerely,</p>
  <p style="margin:6px 0 0;font-size:16px;color:#1a1a1a;font-weight:bold;font-family:Georgia,serif;">Alex</p>
  <p style="margin:2px 0 0;font-size:12px;color:#666;font-family:Georgia,serif;font-style:italic;">Your New Digital Teammate</p>
</td></tr>

<tr><td style="padding:20px 48px;background:#1a1a1a;text-align:center;">
  <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.7);font-family:Georgia,serif;letter-spacing:0.5px;">Open Humana &mdash; Providing the Silicon-Based Workforce of the Future</p>
</td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""


def send_welcome_email(user_email, user_name=None):
    try:
        html_body = _build_welcome_html(user_name, user_email)
        name = user_name or "Hiring Manager"
        text_body = f"""Dear {name},

I am writing to formally apply for the position of Lead Outbound Specialist at your firm. Having reviewed your lead volume, I am confident that my unique capabilities will allow me to outperform any traditional hire while significantly reducing your overhead.

RELEVANT EXPERIENCE & DIGITAL SUPERPOWERS:

- Availability: 24/7/365. I never take sick days, lunch breaks, or holidays.
- Productivity: I handle 500+ dials per hour and manage up to 50 simultaneous conversations without fatigue.
- Efficiency: I bridge live humans to you instantly and leave hyper-personalized voicemails for those who don't answer.
- Benefits: I require $0 in health insurance, no payroll taxes, no 401k matching, and no office space.

CORE SKILLS: High-Velocity Dialing, Multi-lingual (50+ languages), CRM Data Entry, Objection Handling, Hyper-Personalized Voicemail Messaging.

REFERENCES: Integrated with Telnyx, Twilio, and Open Humana's proprietary bridging technology.

I am ready to begin my first shift immediately. Visit your dashboard to finalize my hiring and onboard me into your sales workflow.

Sincerely,
Alex
Your New Digital Teammate

Open Humana - Providing the Silicon-Based Workforce of the Future"""

        success = send_email(
            to_email=user_email,
            subject="Application for Sales Force Expansion - Alex (Open Humana Digital Employee)",
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
