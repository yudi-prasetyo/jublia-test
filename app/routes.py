# app/routes.py
from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import EmailQueue, EmailRecipient
from datetime import datetime
from celery_worker import schedule_email
import pytz

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    The homepage of the application that displays two links to add a new
    email recipient and to queue a new email.
    """
    return render_template('index.html')

@main.route('/save_emails_page')
def save_emails_page():
    """
    The route for the "Queue an Email" page that renders the
    save_emails.html template.
    """
    return render_template('save_emails.html')


@main.route('/add_recipient_page')
def add_recipient_page():
    """
    The route for the "Add an Email Recipient" page that renders the
    add_recipient.html template.
    """
    return render_template('add_recipient.html')

@main.route('/save_emails', methods=['POST'])
def save_emails():
    """
    This route accepts a POST request to save an email to the EmailQueue
    table and schedule it to be sent to the email recipients at the
    specified time.

    Request Body:
        event_id (int): The ID of the event.
        email_subject (str): The subject of the email.
        email_content (str): The body content of the email.
        timestamp (str): The scheduled time for the email to be sent in ISO
            8601 datetime format.
    """
    data = request.get_json()

    event_id = data.get('event_id')
    email_subject = data.get('email_subject')
    email_content = data.get('email_content')
    timestamp_str = data.get('timestamp')

    # Check if the timestamp is in the correct format
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
    except ValueError:
        return jsonify({'error': 'Invalid timestamp format! Please use ISO 8601 format.'}), 400

    # Create a new EmailQueue object and add it to the database
    new_email = EmailQueue(
        event_id=event_id,
        email_subject=email_subject,
        email_content=email_content,
        timestamp=timestamp
    )

    # Get all the email recipients from the database
    recipients = EmailRecipient.query.all()
    r = [recipient.as_dict() for recipient in recipients]

    # Convert the timestamp to the UTC+8 timezone
    utc8 = pytz.timezone('Asia/Singapore')
    timestamp = utc8.localize(timestamp)
    delay_seconds = (timestamp - datetime.now(utc8)).total_seconds()

    # Schedule the email to be sent using Celery
    schedule_email.apply_async((email_subject, email_content, r), countdown=delay_seconds)

    # Commit the changes to the database
    db.session.add(new_email)
    db.session.commit()

    # Return a success message to the user
    return jsonify({'message': 'Email queued successfully!'}), 201

@main.route('/email-recipients', methods=['POST'])
def add_recipient():
    """
    This route accepts a POST request to add a new recipient to the
    EmailRecipient database table.

    Request Body:
        email_address (str): The email address of the recipient.
        full_name (str): The full name of the recipient.
    """
    data = request.get_json()

    email_address = data.get('email_address')
    full_name = data.get('full_name')

    # Create a new EmailRecipient object and add it to the database
    new_recipient = EmailRecipient(
        email_address=email_address,
        full_name=full_name
    )

    db.session.add(new_recipient)
    db.session.commit()

    # Return a success message to the user
    return jsonify({'message': 'Recipient added successfully!'}), 201
