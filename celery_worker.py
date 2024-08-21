from datetime import datetime
from celery import Celery
from celery_config import celery
from mailjet_rest import Client
import os
from app.models import EmailRecipient

@celery.task
def schedule_email(email_subject, email_content, recipients):
    """
    Send an email to the recipients using the Mailjet API.

    Parameters:
    email_subject (str): The subject of the email.
    email_content (str): The content of the email.
    recipients (list): A list of dictionaries containing the recipient's email
        address and full name.
    """
    # Set up the Mailjet API credentials
    api_key = os.environ['MJ_APIKEY_PUBLIC']
    api_secret = os.environ['MJ_APIKEY_PRIVATE']
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    # Create the data to be sent to the Mailjet API
    data = {}
    data["Messages"] = []
    for recipient in recipients:
        data["Messages"].append({
            # Set the sender's email address and name
            "From": {
                "Email": "yudiprasetyo777@gmail.com",
                "Name": "Yudi Prasetyo"
            },
            # Set the recipient's email address and name
            "To": [
                {
                "Email": recipient["email_address"],
                "Name": recipient["full_name"]
                }
            ],
            # Set the subject of the email
            "Subject": email_subject,
            # Set the HTML content of the email
            "HTMLPart": email_content
        })

    # Send the email using the Mailjet API
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
