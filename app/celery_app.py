from celery import Celery
from celery.schedules import crontab
from config import Config

celery = Celery(__name__, backend=Config.CELERY_RESULT_BACKEND, broker=Config.CELERY_BROKER_URL)

def init_celery(app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    # Now you can configure the beat_schedule
    celery.conf.beat_schedule = {
        'send-emails-every-minute': {
            'task': 'app.tasks.send_email_task',
            'schedule': 10.0,
        },
    }

    return celery
