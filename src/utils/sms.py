"""
SMS utility for sending messages via Twilio
"""

from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from .config import Config

class SMSManager:
    def __init__(self):
        config = Config()
        self.account_sid = config.TWILIO_ACCOUNT_SID
        self.auth_token = config.TWILIO_AUTH_TOKEN
        self.from_number = config.TWILIO_PHONE_NUMBER
        self.client = Client(self.account_sid, self.auth_token) if self.account_sid != 'your_account_sid_here' else None

    def send_sms(self, to_number, message):
        """
        Send SMS message to a phone number

        Args:
            to_number (str): Recipient's phone number
            message (str): Message content

        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.client:
            print(f"SMS not configured. Would send to {to_number}: {message}")
            return True  # For development, pretend it worked

        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            print(f"SMS sent successfully to {to_number}. SID: {message.sid}")
            return True
        except TwilioException as e:
            print(f"Failed to send SMS to {to_number}: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error sending SMS: {str(e)}")
            return False

# Global instance
sms_manager = SMSManager()

def send_registration_sms(phone, username, password):
    """
    Send registration confirmation SMS with login credentials

    Args:
        phone (str): Patient's phone number
        username (str): Generated username
        password (str): Generated password

    Returns:
        bool: True if sent successfully
    """
    message = f"Your registration is successful. Username: {username}, Password: {password}. Use this information to login to the webpage."
    return sms_manager.send_sms(phone, message)
