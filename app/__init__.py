from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from .celery_app import init_celery, celery
from app.tasks import send_email_task

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # init_celery(app)  # Initialize Celery with the Flask app context

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
