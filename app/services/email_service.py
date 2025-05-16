import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    @staticmethod
    async def send_email(
        email_to: str,
        subject: str,
        body: str,
        email_from: Optional[str] = None,
    ) -> bool:
        """
        Send an email with the specified parameters.
        Returns True if successful, False otherwise.
        """
        # Use settings if not explicitly provided
        if not email_from:
            email_from = settings.SMTP_FROM_EMAIL
        
        # If SMTP settings are not configured, log and return
        if not all([
            settings.SMTP_SERVER,
            settings.SMTP_PORT,
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD,
            email_from
        ]):
            logger.warning(
                "SMTP settings not fully configured. Email sending is disabled."
            )
            # In development, just log the email content
            if settings.DEBUG:
                logger.info(f"Would send email to: {email_to}")
                logger.info(f"Subject: {subject}")
                logger.info(f"Body: {body}")
                return True
            return False
        
        # Create message
        message = MIMEMultipart()
        message["From"] = email_from
        message["To"] = email_to
        message["Subject"] = subject
        
        # Attach the body
        message.attach(MIMEText(body, "html"))
        
        try:
            # Connect to SMTP server
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()  # Secure the connection
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            
            # Send email
            server.send_message(message)
            server.quit()
            logger.info(f"Email sent successfully to {email_to}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    @staticmethod
    async def send_password_reset_email(email_to: str, token: str, base_url: str) -> bool:
        """
        Send a password reset email with a reset link.
        """
        subject = "Password Reset Request - William Travel"
        reset_link = f"{base_url}/reset-password?token={token}"
        
        # HTML email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
            <h2>Password Reset Request</h2>
            <p>We received a request to reset your password. If you did not make this request, please ignore this email.</p>
            <p>To reset your password, please click the link below:</p>
            <p><a href="{reset_link}" style="padding: 10px 15px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px;">Reset Password</a></p>
            <p>Or copy and paste this link in your browser:</p>
            <p>{reset_link}</p>
            <p>This link will expire in 24 hours.</p>
            <p>Best regards,<br/>William Travel Team</p>
        </body>
        </html>
        """
        
        return await EmailService.send_email(
            email_to=email_to,
            subject=subject,
            body=body
        )
