from flask import Blueprint, request, jsonify
from app import db
from app.models import EmailQueue
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Hello, Flask with PostgreSQL!'

@main.route('/add_email', methods=['POST'])
def add_email():
    data = request.get_json()

    # Extract data from the request
    email_subject = data.get('email_subject')
    email_content = data.get('email_content')
    timestamp = datetime.now()

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