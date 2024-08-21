# from app import db
# from app.models import EmailQueue, EmailRecipient
from celery import shared_task
from datetime import datetime
# from flask_mail import Message, Mail

# mail = Mail()

@shared_task
def send_email_task():
    now = datetime.now()
    print(now)
    # emails_to_send = EmailQueue.query.filter(EmailQueue.timestamp <= now).all()

    # for email in emails_to_send:
    #     recipients = [recipient.email_address for recipient in email.recipients]

    #     if recipients:
    #         msg = Message(
    #             subject=email.email_subject,
    #             recipients=recipients,
    #             body=email.email_content
    #         )
    #         mail.send(msg)

    #         db.session.commit()
