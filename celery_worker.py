from datetime import datetime
from celery import Celery
from celery_config import celery
from mailjet_rest import Client
import os
from app.models import EmailRecipient

@celery.task
def schedule_email(email_subject, email_content, recipients):
    api_key = os.environ['MJ_APIKEY_PUBLIC']
    api_secret = os.environ['MJ_APIKEY_PRIVATE']
    # mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    # data = {}
    # data["Messages"] = []
    # for recipient in recipients:
    #     data["Messages"].append({
    #         "From": {
    #             "Email": "yudiprasetyo777@gmail.com",
    #             "Name": "Yudi Prasetyo"
    #         },
    #         "To": [
    #             {
    #             "Email": recipient["email_address"],
    #             "Name": recipient["full_name"]
    #             }
    #         ],
    #         "Subject": email_subject,
    #         "HTMLPart": email_content
    #     })
    
    # print(data)
    # result = mailjet.send.create(data=data)
    # print(result.status_code)
    # print(result.json())