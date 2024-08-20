from app import db

class EmailQueue(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    email_subject = db.Column(db.String(80), unique=True, nullable=False)
    email_content = db.Column(db.String(120), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<EmailQueue {self.email_subject}>'
