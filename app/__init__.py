# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from celery import Celery

db = SQLAlchemy()

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config.update(
        CELERY_BROKER_URL='redis://redis:6379/0',
        CELERY_RESULT_BACKEND='redis://redis:6379/0'
    )

    celery = make_celery(app)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
