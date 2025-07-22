import logging
import threading
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def send_mail_async(subject, message, from_email, recipient_list, fail_silently=False):
    def task():
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=fail_silently
            )
            logger.info(f"[Email] Successfully sent email to {recipient_list}")
        except Exception as e:
            logger.error(f"[Email ERROR] Failed to send email to {recipient_list}: {e}")
    
    threading.Thread(target=task).start()