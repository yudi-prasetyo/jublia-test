# Email Queue Scheduler

This is a simple Flask application integrated with a PostgreSQL database. The application allows adding email details to a queue via a POST request and stores the information in the database. The email then sends to the recipient via the Mailjet API using Celery worker based on the scheduled time.

## Project Structure

```
jublia-test/
│
├── app/
│   ├── __init__.py           # Application factory and app setup
│   ├── models.py             # SQLAlchemy models
│   └── routes.py             # Routes and view functions
│
├── app.py                    # Main entry point of the application
│
├── celery_config.py          # Celery configuration file
│
├── celery_worker.py          # Celery worker script for scheduling emails
│
├── config.py                 # Configuration file
│
├── docker-compose.yaml       # Docker Compose configuration file
│
├── Dockerfile                # Dockerfile
│
└──requirements.txt          # Python requirements
```

## Requirements

- Docker and Docker Compose installed on your machine
- (Optional) `pgAdmin` or any other PostgreSQL client to access the database

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yudi-prasetyo/jublia-test.git
cd jublia-test
```

### 2. Build and Run the Application

Build and start the application with Docker Compose:

```bash
docker-compose up --build
```

### 3. Access the Application

- Flask App: Access the Flask application at `http://localhost:5000`
- PostgreSQL: The PostgreSQL database is accessible on `localhost:5431`
- Redis: The Redis instance is accessible on `localhost:6379`

### 4. Running Database Migrations

To run database migrations using Flask-Migrate:

```bash
docker-compose exec flask flask db init
docker-compose exec flask flask db migrate -m "Initial migration"
docker-compose exec flask flask db upgrade
```

## Accessing PostgreSQL via pgAdmin
1. Open pgAdmin and log in.
2. Create a new server with the following details:
   - Host name/address: localhost
   - Port: 5431
   - Username: postgres
   - Password: postgre
   - Database: postgres
3. Save and connect.

## API Endpoints

### 1. **Queue an Email**

**Endpoint**: `/save_emails`  
**Method**: `POST`  
**Description**: This endpoint queues an email to be sent later by adding it to the `EmailQueue` database table.

**Request Body**:

```json
{
  "email_subject": "Your Subject Here",
  "email_content": "This is the content of the email.",
  "timestamp": "2024-08-21T12:30:00"
}
```

- **email_subject**: (string, required) The subject of the email.
- **email_content**: (string, required) The body content of the email.
- **timestamp**: (ISO 8601 datetime string, required) The scheduled time for the email to be sent.

**Example Request**:

```bash
curl -X POST http://localhost:5000/save_emails \
-H "Content-Type: application/json" \
-d '{
  "email_subject": "Weekly Update",
  "email_content": "Here is your weekly update...",
  "timestamp": "2024-08-21T12:30:00"
}'
```

**Example Response**:

- **Success (201 Created)**:

```json
{
  "message": "Email queued successfully!"
}
```

- **Failure (400 Bad Request)**:

```json
{
  "error": "Invalid timestamp format! Please use ISO 8601 format."
}
```

---

### 2. **Add an Email Recipient**

**Endpoint**: `/email-recipients`  
**Method**: `POST`  
**Description**: This endpoint adds a new recipient to the `EmailRecipient` database table.

**Request Body**:

```json
{
  "email_address": "recipient@example.com",
  "full_name": "Recipient Name"
}
```

- **email_address**: (string, required) The email address of the recipient.
- **full_name**: (string, required) The full name of the recipient.

**Example Request**:

```bash
curl -X POST http://localhost:5000/email-recipients \
-H "Content-Type: application/json" \
-d '{
  "email_address": "recipient@example.com",
  "full_name": "John Doe"
}'
```

**Example Response**:

- **Success (201 Created)**:

```json
{
  "message": "Recipient added successfully!"
}
```

## Project Dependencies
- Flask
- Flask-SQLAlchemy
- psycopg2-binary
- Flask-Migrate
- python-dotenv
- celery
- redis
- pytz
- mailjet_rest