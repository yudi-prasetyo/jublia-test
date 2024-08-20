from flask import Blueprint, request, jsonify
from app import db
from app.models import EmailQueue, EmailRecipient
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Hello, Flask with PostgreSQL!'

@main.route('/save_emails', methods=['POST'])
def save_emails():
    data = request.get_json()

    # Extract data from the request
    email_subject = data.get('email_subject')
    email_content = data.get('email_content')
    timestamp_str = data.get('timestamp')

    # Convert timestamp string to datetime object
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
    except ValueError:
        return jsonify({'error': 'Invalid timestamp format! Please use ISO 8601 format.'}), 400

    # Create a new EmailQueue instance
    new_email = EmailQueue(
        email_subject=email_subject,
        email_content=email_content,
        timestamp=timestamp
    )

    # Add and commit the new record to the database
    db.session.add(new_email)
    db.session.commit()

    return jsonify({'message': 'Email queued successfully!'}), 201

@main.route('/email-recipients', methods=['POST'])
def add_recipient():
    data = request.get_json()

    # Extract data from the request
    email_address = data.get('email_address')
    full_name = data.get('full_name')

    # Create a new EmailRecipient instance
    new_recipient = EmailRecipient(
        email_address=email_address,
        full_name=full_name
    )

    # Add and commit the new recipient to the database
    db.session.add(new_recipient)
    db.session.commit()

    return jsonify({'message': 'Recipient added successfully!'}), 201