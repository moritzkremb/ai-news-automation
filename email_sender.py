"""
Email Sender Module

Handles sending email digests with AI news content.
"""

import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any


class EmailSender:
    """Handles email sending functionality."""
    
    def __init__(self, email_config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.config = email_config
        
        # Get email credentials from environment variables
        self.smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = email_config.get('smtp_port', 587)
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')  # App password for Gmail
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate email configuration."""
        required_vars = ['SENDER_EMAIL', 'SENDER_PASSWORD', 'RECIPIENT_EMAIL']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        self.logger.info("Email configuration validated successfully")
    
    def send_digest(self, subject: str, html_content: str):
        """Send the daily AI news digest email."""
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            
            # Create plain text version
            plain_content = self._html_to_plain(html_content)
            
            # Attach both versions
            text_part = MIMEText(plain_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            message.attach(text_part)
            message.attach(html_part)
            
            # Send email
            self._send_email(message)
            
            self.logger.info(f"Email sent successfully to {self.recipient_email}")
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            raise
    
    def _send_email(self, message: MIMEMultipart):
        """Send email using SMTP."""
        try:
            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable security
                server.login(self.sender_email, self.sender_password)
                
                # Send email
                text = message.as_string()
                server.sendmail(self.sender_email, self.recipient_email, text)
                
        except smtplib.SMTPAuthenticationError:
            raise Exception("SMTP Authentication failed. Check your email credentials and app password.")
        except smtplib.SMTPRecipientsRefused:
            raise Exception(f"Recipient email address rejected: {self.recipient_email}")
        except smtplib.SMTPServerDisconnected:
            raise Exception("SMTP server connection was unexpectedly closed.")
        except Exception as e:
            raise Exception(f"SMTP error occurred: {str(e)}")
    
    def _html_to_plain(self, html_content: str) -> str:
        """Convert HTML content to plain text for email clients that don't support HTML."""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except ImportError:
            # Fallback: simple HTML tag removal
            import re
            text = re.sub('<[^<]+?>', '', html_content)
            return text.strip()
        except Exception as e:
            self.logger.warning(f"Error converting HTML to plain text: {str(e)}")
            return "AI News Digest - Please view in HTML format"
    
    def send_test_email(self):
        """Send a test email to verify configuration."""
        try:
            subject = "AI News Bot - Test Email"
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 20px; }}
                    .test-message {{ background: #e8f5e8; padding: 15px; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="test-message">
                    <h2>Test Email Successful!</h2>
                    <p>Your AI News Bot is configured correctly and ready to send daily digests.</p>
                    <p><strong>Configuration Details:</strong></p>
                    <ul>
                        <li>SMTP Server: {self.smtp_server}:{self.smtp_port}</li>
                        <li>Sender: {self.sender_email}</li>
                        <li>Recipient: {self.recipient_email}</li>
                    </ul>
                </div>
            </body>
            </html>
            """
            
            self.send_digest(subject, html_content)
            return True
            
        except Exception as e:
            self.logger.error(f"Test email failed: {str(e)}")
            return False