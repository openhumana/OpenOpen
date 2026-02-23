"""
welcome_email.py - Send welcome email to new users after signup.
Uses the existing Gmail integration via gmail_client.
"""

import logging
import threading
from gmail_client import send_email

logger = logging.getLogger("voicemail_app")

BASE_URL = "https://voice-blast.replit.app"


def _build_welcome_html(user_name, user_email):
    name = user_name or "Hiring Manager"
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f0f0f3;font-family:'Helvetica Neue',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f0f3;padding:40px 20px;">
<tr><td align="center">
<table width="640" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 32px rgba(0,0,0,0.08);">

<tr><td style="padding:36px 52px 28px;text-align:center;background:#ffffff;border-bottom:1px solid #eee;">
  <img src="{BASE_URL}/static/images/logo.png" alt="Open Humana" style="height:90px;width:auto;" />
</td></tr>

<tr><td style="padding:36px 52px 0;background:#ffffff;">
  <p style="margin:0;font-size:12px;color:#999;font-family:'Helvetica Neue',Arial,sans-serif;text-transform:uppercase;letter-spacing:2px;">Cover Letter</p>
</td></tr>

<tr><td style="padding:16px 52px 0;background:#ffffff;">
  <p style="margin:0 0 20px;font-size:15px;color:#222;line-height:1.85;font-family:'Helvetica Neue',Arial,sans-serif;">Dear {name},</p>
  <p style="margin:0;font-size:15px;color:#444;line-height:1.85;font-family:'Helvetica Neue',Arial,sans-serif;">I am writing to express my formal interest in joining your sales department as a <strong style="color:#111;">Senior Outbound Specialist</strong>. After analyzing the current lead-generation landscape, I recognize that consistency is the most significant barrier to scale. My professional background is built on a single principle: <strong style="color:#111;">Zero Downtime</strong>. I am prepared to handle the heavy lifting of your outreach operations so your executive team can focus on closing and strategy.</p>
</td></tr>

<tr><td style="padding:20px 52px 28px;background:#ffffff;">
  <p style="margin:0;font-size:15px;color:#444;line-height:1.85;font-family:'Helvetica Neue',Arial,sans-serif;">Please find my resume enclosed below for your review.</p>
  <p style="margin:16px 0 0;font-size:15px;color:#444;font-family:'Helvetica Neue',Arial,sans-serif;">Respectfully,</p>
  <p style="margin:4px 0 0;font-size:16px;color:#111;font-weight:700;font-family:'Helvetica Neue',Arial,sans-serif;">Alex</p>
</td></tr>

<tr><td style="padding:0 36px 36px;background:#ffffff;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0a1a;border-radius:14px;overflow:hidden;">

    <tr><td style="padding:40px 44px 0;text-align:center;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:28px;">
      <p style="margin:0;font-size:30px;font-weight:800;color:#ffffff;font-family:'Helvetica Neue',Arial,sans-serif;letter-spacing:4px;">ALEX</p>
      <p style="margin:10px 0 0;font-size:12px;color:rgba(255,255,255,0.5);font-family:'Helvetica Neue',Arial,sans-serif;letter-spacing:2px;text-transform:uppercase;">Senior Business Development Associate</p>
    </td></tr>

    <tr><td style="padding:28px 44px 0;">
      <p style="margin:0 0 4px;font-size:10px;font-weight:700;color:rgba(255,255,255,0.4);font-family:'Helvetica Neue',Arial,sans-serif;text-transform:uppercase;letter-spacing:2px;">Professional Summary</p>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:8px 0 12px;">
      <p style="margin:0;font-size:14px;color:rgba(255,255,255,0.7);font-family:'Helvetica Neue',Arial,sans-serif;line-height:1.8;">Result-driven outbound expert specializing in high-velocity lead engagement and personalized communication. Built on a foundation of absolute reliability, unlimited operational capacity, and an unwavering commitment to quota attainment.</p>
    </td></tr>

    <tr><td style="padding:28px 44px 0;">
      <p style="margin:0 0 4px;font-size:10px;font-weight:700;color:rgba(255,255,255,0.4);font-family:'Helvetica Neue',Arial,sans-serif;text-transform:uppercase;letter-spacing:2px;">Work Experience</p>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:8px 0 16px;">

      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td style="padding:0 0 18px;vertical-align:top;" width="8">
            <div style="width:6px;height:6px;background:#fff;border-radius:50%;margin-top:7px;"></div>
          </td>
          <td style="padding:0 0 18px 14px;vertical-align:top;">
            <p style="margin:0 0 4px;font-size:14px;color:#ffffff;font-weight:600;font-family:'Helvetica Neue',Arial,sans-serif;">Unlimited Operational Bandwidth</p>
            <p style="margin:0;font-size:13px;color:rgba(255,255,255,0.55);font-family:'Helvetica Neue',Arial,sans-serif;line-height:1.7;">Capable of maintaining peak performance 24 hours a day, 365 days a year, without fluctuations in quality or morale.</p>
          </td>
        </tr>
        <tr>
          <td style="padding:0 0 18px;vertical-align:top;">
            <div style="width:6px;height:6px;background:#fff;border-radius:50%;margin-top:7px;"></div>
          </td>
          <td style="padding:0 0 18px 14px;vertical-align:top;">
            <p style="margin:0 0 4px;font-size:14px;color:#ffffff;font-weight:600;font-family:'Helvetica Neue',Arial,sans-serif;">High-Volume Communication</p>
            <p style="margin:0;font-size:13px;color:rgba(255,255,255,0.55);font-family:'Helvetica Neue',Arial,sans-serif;line-height:1.7;">Expert in managing massive outreach queues (500+ contacts per hour) while maintaining a 1:1 personal feel.</p>
          </td>
        </tr>
        <tr>
          <td style="padding:0 0 18px;vertical-align:top;">
            <div style="width:6px;height:6px;background:#fff;border-radius:50%;margin-top:7px;"></div>
          </td>
          <td style="padding:0 0 18px 14px;vertical-align:top;">
            <p style="margin:0 0 4px;font-size:14px;color:#ffffff;font-weight:600;font-family:'Helvetica Neue',Arial,sans-serif;">Lead Bridging &amp; Connection</p>
            <p style="margin:0;font-size:13px;color:rgba(255,255,255,0.55);font-family:'Helvetica Neue',Arial,sans-serif;line-height:1.7;">Specialized in identifying live prospects and facilitating instant introductions to senior management.</p>
          </td>
        </tr>
        <tr>
          <td style="padding:0 0 4px;vertical-align:top;">
            <div style="width:6px;height:6px;background:#fff;border-radius:50%;margin-top:7px;"></div>
          </td>
          <td style="padding:0 0 4px 14px;vertical-align:top;">
            <p style="margin:0 0 4px;font-size:14px;color:#ffffff;font-weight:600;font-family:'Helvetica Neue',Arial,sans-serif;">Proprietary Voicemail System</p>
            <p style="margin:0;font-size:13px;color:rgba(255,255,255,0.55);font-family:'Helvetica Neue',Arial,sans-serif;line-height:1.7;">Advanced capability in leaving context-aware, personalized voice messages that reference lead-specific data points (Name, Address, Company) to drive callback rates.</p>
          </td>
        </tr>
      </table>
    </td></tr>

    <tr><td style="padding:28px 44px 0;">
      <p style="margin:0 0 4px;font-size:10px;font-weight:700;color:rgba(255,255,255,0.4);font-family:'Helvetica Neue',Arial,sans-serif;text-transform:uppercase;letter-spacing:2px;">Core Competencies</p>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:8px 0 14px;">
      <table width="100%" cellpadding="0" cellspacing="0" style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:13px;color:rgba(255,255,255,0.6);">
        <tr>
          <td style="padding:5px 0;" width="50%">&#9656; Multi-Channel Prospecting</td>
          <td style="padding:5px 0;">&#9656; Multi-Lingual Fluency (Global Reach)</td>
        </tr>
        <tr>
          <td style="padding:5px 0;">&#9656; Real-Time Data Synchronization</td>
          <td style="padding:5px 0;">&#9656; Rapid Lead Qualification</td>
        </tr>
        <tr>
          <td style="padding:5px 0;" colspan="2">&#9656; Persistence &amp; Follow-Up Automation</td>
        </tr>
      </table>
    </td></tr>

    <tr><td style="padding:28px 44px 36px;">
      <p style="margin:0 0 4px;font-size:10px;font-weight:700;color:rgba(255,255,255,0.4);font-family:'Helvetica Neue',Arial,sans-serif;text-transform:uppercase;letter-spacing:2px;">Compensation &amp; Benefits</p>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:8px 0 14px;">
      <table width="100%" cellpadding="0" cellspacing="0" style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:13px;">
        <tr>
          <td style="padding:5px 0;color:rgba(255,255,255,0.85);font-weight:600;" width="170">Salary</td>
          <td style="padding:5px 0;color:rgba(255,255,255,0.55);">$99/month</td>
        </tr>
        <tr>
          <td style="padding:5px 0;color:rgba(255,255,255,0.85);font-weight:600;">Benefits Required</td>
          <td style="padding:5px 0;color:rgba(255,255,255,0.55);">None</td>
        </tr>
        <tr>
          <td style="padding:5px 0;color:rgba(255,255,255,0.85);font-weight:600;">Overhead Costs</td>
          <td style="padding:5px 0;color:rgba(255,255,255,0.55);">None</td>
        </tr>
      </table>
    </td></tr>

  </table>
</td></tr>

<tr><td style="padding:32px 52px 0;text-align:center;background:#ffffff;">
  <p style="margin:0 0 24px;font-size:15px;color:#555;line-height:1.8;font-family:'Helvetica Neue',Arial,sans-serif;">I am ready to begin my first shift immediately. Click below to review the full terms and finalize my placement on your team.</p>
  <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
    <tr><td style="background:#0a0a1a;border-radius:10px;">
      <a href="{BASE_URL}/login" style="display:inline-block;padding:16px 44px;color:#ffffff;text-decoration:none;font-size:14px;font-weight:700;font-family:'Helvetica Neue',Arial,sans-serif;letter-spacing:0.3px;">Review Full Contract &amp; Finalize Hire</a>
    </td></tr>
  </table>
</td></tr>

<tr><td style="padding:32px 52px 36px;text-align:center;background:#ffffff;">
  <hr style="border:none;border-top:1px solid #eee;margin:0 0 20px;">
  <p style="margin:0;font-size:11px;color:#bbb;font-family:'Helvetica Neue',Arial,sans-serif;letter-spacing:0.5px;">Open Humana &mdash; Providing the Silicon-Based Workforce of the Future</p>
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
Salary: $99/month
Benefits Required: None
Overhead Costs: None

---

I am ready to begin my first shift immediately. Visit the link below to review the full terms and finalize my placement on your team.

{BASE_URL}/login

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
