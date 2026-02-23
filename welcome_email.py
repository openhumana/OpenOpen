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
<body style="margin:0;padding:0;background:#ededed;font-family:Georgia,'Times New Roman',Times,serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#ededed;padding:48px 20px;">
<tr><td align="center">
<table width="640" cellpadding="0" cellspacing="0" style="background:#ffffff;border:1px solid #c0c0c0;">

<tr><td style="padding:44px 56px 0;text-align:right;">
  <span style="font-size:12px;color:#777;font-family:Georgia,serif;">February 2026</span>
</td></tr>

<tr><td style="padding:28px 56px 0;">
  <p style="margin:0 0 20px;font-size:15px;color:#222;line-height:1.8;font-family:Georgia,serif;">Dear {name},</p>
  <p style="margin:0;font-size:15px;color:#222;line-height:1.85;font-family:Georgia,serif;">I am writing to express my formal interest in joining your sales department as a <strong>Senior Outbound Specialist</strong>. After analyzing the current lead-generation landscape, I recognize that consistency is the most significant barrier to scale. My professional background is built on a single principle: <strong>Zero Downtime</strong>. I am prepared to handle the heavy lifting of your outreach operations so your executive team can focus on closing and strategy.</p>
  <p style="margin:20px 0 0;font-size:15px;color:#222;line-height:1.85;font-family:Georgia,serif;">Please find my resume enclosed below for your review. I welcome the opportunity to discuss how my capabilities align with your growth objectives.</p>
</td></tr>

<tr><td style="padding:20px 56px;">
  <p style="margin:0;font-size:15px;color:#222;font-family:Georgia,serif;">Respectfully,</p>
  <p style="margin:6px 0 0;font-size:16px;color:#111;font-weight:bold;font-family:Georgia,serif;">Alex</p>
</td></tr>

<tr><td style="padding:0 56px;">
  <hr style="border:none;border-top:1px solid #ccc;margin:0;">
</td></tr>

<tr><td style="padding:36px 56px 0;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;border:2px solid #222;">

    <tr><td style="padding:32px 36px 0;text-align:center;">
      <p style="margin:0;font-size:26px;font-weight:bold;color:#111;font-family:Georgia,serif;letter-spacing:2px;">ALEX</p>
      <p style="margin:6px 0 0;font-size:13px;color:#555;font-family:Georgia,serif;letter-spacing:1.5px;text-transform:uppercase;">Senior Business Development Associate</p>
      <hr style="border:none;border-top:2px solid #111;margin:20px 0 0;">
    </td></tr>

    <tr><td style="padding:20px 36px 0;">
      <p style="margin:0 0 8px;font-size:12px;font-weight:bold;color:#111;font-family:Georgia,serif;text-transform:uppercase;letter-spacing:1.5px;">Professional Summary</p>
      <p style="margin:0;font-size:14px;color:#333;font-family:Georgia,serif;line-height:1.8;">Result-driven outbound expert specializing in high-velocity lead engagement and personalized communication. Built on a foundation of absolute reliability, unlimited operational capacity, and an unwavering commitment to quota attainment.</p>
    </td></tr>

    <tr><td style="padding:24px 36px 0;">
      <p style="margin:0 0 14px;font-size:12px;font-weight:bold;color:#111;font-family:Georgia,serif;text-transform:uppercase;letter-spacing:1.5px;">Work Experience</p>

      <p style="margin:0 0 6px;font-size:14px;color:#111;font-weight:bold;font-family:Georgia,serif;">Unlimited Operational Bandwidth</p>
      <p style="margin:0 0 14px;font-size:13px;color:#444;font-family:Georgia,serif;line-height:1.8;padding-left:16px;">Capable of maintaining peak performance 24 hours a day, 365 days a year, without fluctuations in quality or morale.</p>

      <p style="margin:0 0 6px;font-size:14px;color:#111;font-weight:bold;font-family:Georgia,serif;">High-Volume Communication</p>
      <p style="margin:0 0 14px;font-size:13px;color:#444;font-family:Georgia,serif;line-height:1.8;padding-left:16px;">Expert in managing massive outreach queues (500+ contacts per hour) while maintaining a 1:1 personal feel.</p>

      <p style="margin:0 0 6px;font-size:14px;color:#111;font-weight:bold;font-family:Georgia,serif;">Lead Bridging &amp; Connection</p>
      <p style="margin:0 0 14px;font-size:13px;color:#444;font-family:Georgia,serif;line-height:1.8;padding-left:16px;">Specialized in identifying live prospects and facilitating instant introductions to senior management.</p>

      <p style="margin:0 0 6px;font-size:14px;color:#111;font-weight:bold;font-family:Georgia,serif;">Proprietary Voicemail System</p>
      <p style="margin:0 0 4px;font-size:13px;color:#444;font-family:Georgia,serif;line-height:1.8;padding-left:16px;">Advanced capability in leaving context-aware, personalized voice messages that reference lead-specific data points (Name, Address, Company) to drive callback rates.</p>
    </td></tr>

    <tr><td style="padding:24px 36px 0;">
      <p style="margin:0 0 12px;font-size:12px;font-weight:bold;color:#111;font-family:Georgia,serif;text-transform:uppercase;letter-spacing:1.5px;">Core Competencies</p>
      <table width="100%" cellpadding="0" cellspacing="0" style="font-family:Georgia,serif;font-size:13px;color:#333;">
        <tr>
          <td style="padding:4px 0;" width="50%">&#8226; Multi-Channel Prospecting</td>
          <td style="padding:4px 0;">&#8226; Multi-Lingual Fluency (Global Reach)</td>
        </tr>
        <tr>
          <td style="padding:4px 0;">&#8226; Real-Time Data Synchronization</td>
          <td style="padding:4px 0;">&#8226; Rapid Lead Qualification</td>
        </tr>
        <tr>
          <td style="padding:4px 0;" colspan="2">&#8226; Persistence &amp; Follow-Up Automation</td>
        </tr>
      </table>
    </td></tr>

    <tr><td style="padding:24px 36px;">
      <p style="margin:0 0 12px;font-size:12px;font-weight:bold;color:#111;font-family:Georgia,serif;text-transform:uppercase;letter-spacing:1.5px;">Compensation &amp; Benefits</p>
      <table width="100%" cellpadding="0" cellspacing="0" style="font-family:Georgia,serif;font-size:13px;color:#333;">
        <tr>
          <td style="padding:4px 0;" width="180"><strong>Annual Salary:</strong></td>
          <td style="padding:4px 0;">$1,188 ($99 billed monthly)</td>
        </tr>
        <tr>
          <td style="padding:4px 0;"><strong>Insurance / Taxes:</strong></td>
          <td style="padding:4px 0;">Fully waived</td>
        </tr>
        <tr>
          <td style="padding:4px 0;"><strong>PTO / Sick Leave:</strong></td>
          <td style="padding:4px 0;">None required</td>
        </tr>
      </table>
    </td></tr>

  </table>
</td></tr>

<tr><td style="padding:36px 56px 0;text-align:center;">
  <p style="margin:0 0 20px;font-size:15px;color:#222;line-height:1.8;font-family:Georgia,serif;">I am ready to begin my first shift immediately. Please click below to review the full terms and finalize my placement on your team.</p>
  <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
    <tr><td style="background:#111111;border-radius:4px;">
      <a href="https://voice-blast.replit.app/login" style="display:inline-block;padding:16px 40px;color:#ffffff;text-decoration:none;font-size:14px;font-weight:bold;font-family:Georgia,serif;letter-spacing:0.5px;">Review Full Contract &amp; Finalize Hire</a>
    </td></tr>
  </table>
</td></tr>

<tr><td style="padding:36px 56px 20px;text-align:center;">
  <hr style="border:none;border-top:1px solid #ddd;margin:0 0 20px;">
  <p style="margin:0;font-size:11px;color:#999;font-family:Georgia,serif;letter-spacing:0.3px;">Open Humana &mdash; Providing the Silicon-Based Workforce of the Future</p>
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

I am writing to express my formal interest in joining your sales department as a Senior Outbound Specialist. After analyzing the current lead-generation landscape, I recognize that consistency is the most significant barrier to scale. My professional background is built on a single principle: Zero Downtime. I am prepared to handle the heavy lifting of your outreach operations so your executive team can focus on closing and strategy.

Please find my resume below for your review.

Respectfully,
Alex

---

ALEX
Senior Business Development Associate

PROFESSIONAL SUMMARY
Result-driven outbound expert specializing in high-velocity lead engagement and personalized communication. Built on a foundation of absolute reliability, unlimited operational capacity, and an unwavering commitment to quota attainment.

WORK EXPERIENCE

Unlimited Operational Bandwidth
Capable of maintaining peak performance 24 hours a day, 365 days a year, without fluctuations in quality or morale.

High-Volume Communication
Expert in managing massive outreach queues (500+ contacts per hour) while maintaining a 1:1 personal feel.

Lead Bridging & Connection
Specialized in identifying live prospects and facilitating instant introductions to senior management.

Proprietary Voicemail System
Advanced capability in leaving context-aware, personalized voice messages that reference lead-specific data points (Name, Address, Company) to drive callback rates.

CORE COMPETENCIES
- Multi-Channel Prospecting
- Multi-Lingual Fluency (Global Reach)
- Real-Time Data Synchronization
- Rapid Lead Qualification
- Persistence & Follow-Up Automation

COMPENSATION & BENEFITS
Annual Salary: $1,188 ($99 billed monthly)
Insurance / Taxes: Fully waived
PTO / Sick Leave: None required

---

I am ready to begin my first shift immediately. Visit the link below to review the full terms and finalize my placement on your team.

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
