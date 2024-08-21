from datetime import datetime
from celery import Celery
from celery_config import celery

@celery.task
def run_every_five_seconds():
    print("Task running every 5 seconds")

@celery.task
def schedule_email():
    now = datetime.now()
    print("Email sent at: ", now)

# Schedule the task to run every 5 seconds
# celery.conf.beat_schedule = {
#     'run-every-5-seconds': {
#         'task': 'celery_worker.run_every_five_seconds',
#         'schedule': 5.0,  # seconds
#     },
# }

# if __name__ == '__main__':
#     celery.start()
