import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        pass
        
    def send_email(self, to_email, subject, body):
        """Send email notification"""
        logger.info(f"Sending email to {to_email}: {subject}")
        return True
    
    def send_push_notification(self, user_id, message, data=None):
        """Send push notification"""
        logger.info(f"Sending push to {user_id}: {message}")
        return True
    
    def send_sms(self, phone_number, message):
        """Send SMS notification"""
        logger.info(f"Sending SMS to {phone_number}: {message}")
        return True
    
    def send_emergency_alert(self, user_id, location, emergency_type):
        """Send emergency alert"""
        logger.info(f"EMERGENCY: {emergency_type} at {location}")
        return True
