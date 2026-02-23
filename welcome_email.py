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
<body style="margin:0;padding:0;background:#0a0a1a;font-family:'Helvetica Neue',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0a1a;padding:40px 20px;">
<tr><td align="center">
<table width="640" cellpadding="0" cellspacing="0" style="background:#0a0a1a;">

<tr><td style="padding:32px 0;text-align:center;">
  <img src="{BASE_URL}/static/images/logo.png" alt="Open Humana" style="height:80px;width:auto;" />
</td></tr>

<tr><td>
<table width="100%" cellpadding="0" cellspacing="0" style="background:#111118;border:1px solid rgba(255,255,255,0.08);border-radius:16px;overflow:hidden;">

<tr><td style="background:linear-gradient(135deg,#0a0a1a 0%,#1a1a2e 50%,#0a0a1a 100%);padding:48px 52px 36px;text-align:center;">
  <p style="margin:0 0 6px;font-size:12px;color:rgba(255,255,255,0.35);font-family:'Helvetica Neue',Arial,sans-serif;text-transform:uppercase;letter-spacing:2px;">Cover Letter</p>
  <h1 style="margin:0;font-size:28px;font-weight:800;color:#ffffff;letter-spacing:-0.5px;font-family:'Helvetica Neue',Arial,sans-serif;">Application for Senior Outbound Specialist</h1>
  <p style="margin:12px auto 0;font-size:14px;color:rgba(255,255,255,0.5);max-width:400px;line-height:1.6;">Submitted by Alex &mdash; Your Digital Teammate</p>
</td></tr>

<tr><td style="padding:40px 52px 0;">
  <p style="margin:0 0 20px;font-size:15px;color:rgba(255,255,255,0.85);line-height:1.85;font-family:'Helvetica Neue',Arial,sans-serif;">Dear {name},</p>
  <p style="margin:0;font-size:15px;color:rgba(255,255,255,0.7);line-height:1.85;font-family:'Helvetica Neue',Arial,sans-serif;">I am writing to express my formal interest in joining your sales department as a <span style="color:#fff;font-weight:600;">Senior Outbound Specialist</span>. After analyzing the current lead-generation landscape, I recognize that consistency is the most significant barrier to scale. My professional background is built on a single principle: <span style="color:#fff;font-weight:600;">Zero Downtime</span>. I am prepared to handle the heavy lifting of your outreach operations so your executive team can focus on closing and strategy.</p>
</td></tr>

<tr><td style="padding:20px 52px 32px;">
  <p style="margin:0;font-size:15px;color:rgba(255,255,255,0.7);line-height:1.85;font-family:'Helvetica Neue',Arial,sans-serif;">Please find my resume enclosed below for your review.</p>
  <p style="margin:16px 0 0;font-size:15px;color:rgba(255,255,255,0.7);font-family:'Helvetica Neue',Arial,sans-serif;">Respectfully,</p>
  <p style="margin:4px 0 0;font-size:16px;color:#ffffff;font-weight:700;font-family:'Helvetica Neue',Arial,sans-serif;">Alex</p>
</td></tr>

<tr><td style="padding:0 40px;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0d0d1a;border:1px solid rgba(255,255,255,0.1);border-radius:12px;overflow:hidden;">

    <tr><td style="padding:36px 40px 0;text-align:center;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:28px;">
      <p style="margin:0;font-size:28px;font-weight:800;color:#ffffff;font-family:'Helvetica Neue',Arial,sans-serif;letter-spacing:3px;">ALEX</p>
      <p style="margin:8px 0 0;font-size:12px;color:rgba(255,255,255,0.45);font-family:'Helvetica Neue',Arial,sans-serif;letter-spacing:2px;text-transform:uppercase;">Senior Business Development Associate</p>
    </td></tr>

    <tr><td style="padding:28px 40px 0;">
      <p style="margin:0 0 4px;font-size:10px;font-weight:700;color:rgba(255,255,255,0.35);font-family:'Helvetica Neue',Arial,sans-serif;text-transform:uppercase;letter-spacing:2px;">Professional Summary</p>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:8px 0 12px;">
      <p style="margin:0;font-size:14px;color:rgba(255,255,255,0.65);font-family:'Helvetica Neue',Arial,sans-serif;line-height:1.8;">Result-driven outbound expert specializing in high-velocity lead engagement and personalized communication. Built on a foundation of absolute reliability, unlimited operational capacity, and an unwavering commitment to quota attainment.</p>
    </td></tr>

    <tr><td style="padding:28px 40px 0;">
      <p style="margin:0 0 4px;font-size:10px;font-weight:700;color:rgba(255,255,255,0.35);font-family:'Helvetica Neue',Arial,sans-serif;text-transform:uppercase;letter-spacing:2px;">Work Experience</p>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:8px 0 16px;">

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

    <tr><td style="padding:28px 40px 0;">
      <p style="margin:0 0 4px;font-size:10px;font-weight:700;color:rgba(255,255,255,0.35);font-family:'Helvetica Neue',Arial,sans-serif;text-transform:uppercase;letter-spacing:2px;">Core Competencies</p>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:8px 0 14px;">
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

    <tr><td style="padding:28px 40px 32px;">
      <p style="margin:0 0 4px;font-size:10px;font-weight:700;color:rgba(255,255,255,0.35);font-family:'Helvetica Neue',Arial,sans-serif;text-transform:uppercase;letter-spacing:2px;">Compensation &amp; Benefits</p>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:8px 0 14px;">
      <table width="100%" cellpadding="0" cellspacing="0" style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:13px;">
        <tr>
          <td style="padding:5px 0;color:rgba(255,255,255,0.8);font-weight:600;" width="170">Salary</td>
          <td style="padding:5px 0;color:rgba(255,255,255,0.55);">$99/month</td>
        </tr>
        <tr>
          <td style="padding:5px 0;color:rgba(255,255,255,0.8);font-weight:600;">Benefits Required</td>
          <td style="padding:5px 0;color:rgba(255,255,255,0.55);">None</td>
        </tr>
        <tr>
          <td style="padding:5px 0;color:rgba(255,255,255,0.8);font-weight:600;">Overhead Costs</td>
          <td style="padding:5px 0;color:rgba(255,255,255,0.55);">None</td>
        </tr>
      </table>
    </td></tr>

  </table>
</td></tr>

<tr><td style="padding:36px 52px 0;text-align:center;">
  <p style="margin:0 0 24px;font-size:15px;color:rgba(255,255,255,0.65);line-height:1.8;font-family:'Helvetica Neue',Arial,sans-serif;">I am ready to begin my first shift immediately. Click below to review the full terms and finalize my placement on your team.</p>
  <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
    <tr><td style="background:#ffffff;border-radius:10px;">
      <a href="{BASE_URL}/login" style="display:inline-block;padding:16px 44px;color:#0a0a1a;text-decoration:none;font-size:14px;font-weight:700;font-family:'Helvetica Neue',Arial,sans-serif;letter-spacing:0.3px;">Review Full Contract &amp; Finalize Hire</a>
    </td></tr>
  </table>
</td></tr>

<tr><td style="padding:40px 52px 36px;text-align:center;">
  <hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 0 24px;">
  <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.3);font-family:'Helvetica Neue',Arial,sans-serif;letter-spacing:0.5px;">Open Humana &mdash; Providing the Silicon-Based Workforce of the Future</p>
</td></tr>

</table>
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
