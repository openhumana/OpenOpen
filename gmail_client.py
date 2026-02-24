"""
gmail_client.py - Gmail SMTP integration via App Password.
Sends emails using openhumana@gmail.com through Gmail SMTP with app password.
"""

import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

logger = logging.getLogger("voicemail_app")

GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "openhumana@gmail.com")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(to_email, subject, html_body, text_body=None, csv_attachment=None, csv_filename=None):
    try:
        if not GMAIL_APP_PASSWORD:
            logger.error("GMAIL_APP_PASSWORD not set")
            return False

        msg = MIMEMultipart("mixed")
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject

        alt = MIMEMultipart("alternative")
        if text_body:
            alt.attach(MIMEText(text_body, "plain", "utf-8"))
        alt.attach(MIMEText(html_body, "html", "utf-8"))
        msg.attach(alt)

        if csv_attachment and csv_filename:
            part = MIMEBase("text", "csv")
            part.set_payload(csv_attachment.encode("utf-8"))
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={csv_filename}")
            msg.attach(part)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_bytes())

        logger.info(f"Email sent successfully to {to_email}: {subject}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False


def test_connection():
    try:
        if not GMAIL_APP_PASSWORD:
            return {"connected": False, "error": "GMAIL_APP_PASSWORD not set"}

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)

        return {"connected": True, "email": GMAIL_ADDRESS}
    except Exception as e:
        return {"connected": False, "error": str(e)}
