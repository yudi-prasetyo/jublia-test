# app/routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models import EmailQueue, EmailRecipient
from datetime import datetime
from celery_worker import schedule_email
import pytz

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Hello, Flask with PostgreSQL!'

@main.route('/save_emails', methods=['POST'])
def save_emails():
    data = request.get_json()

    event_id = data.get('event_id')
    email_subject = data.get('email_subject')
    email_content = data.get('email_content')
    timestamp_str = data.get('timestamp')

    try:
        timestamp = datetime.fromisoformat(timestamp_str)
    except ValueError:
        return jsonify({'error': 'Invalid timestamp format! Please use ISO 8601 format.'}), 400

    new_email = EmailQueue(
        event_id=event_id,
        email_subject=email_subject,
        email_content=email_content,
        timestamp=timestamp
    )

    recipients = EmailRecipient.query.all()
    r = [recipient.as_dict() for recipient in recipients]

    utc8 = pytz.timezone('Asia/Singapore')
    timestamp = utc8.localize(timestamp)
    delay_seconds = (timestamp - datetime.now(utc8)).total_seconds()

    schedule_email.apply_async((email_subject, email_content, r), countdown=delay_seconds)

    db.session.add(new_email)
    db.session.commit()

    return jsonify({'message': 'Email queued successfully!'}), 201

@main.route('/email-recipients', methods=['POST'])
def add_recipient():
    data = request.get_json()

    email_address = data.get('email_address')
    full_name = data.get('full_name')

    new_recipient = EmailRecipient(
        email_address=email_address,
        full_name=full_name
    )

    db.session.add(new_recipient)
    db.session.commit()

    return jsonify({'message': 'Recipient added successfully!'}), 201
