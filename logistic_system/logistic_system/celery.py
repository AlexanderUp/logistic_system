import logging
import os

from celery import Celery
from celery.schedules import crontab

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistic_system.settings')

app = Celery('logistic_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'randomize_vehicle_position': {
        'task': 'tracks.tasks.randomize_vehicle_position_task',
        'schedule': crontab(),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    logger.info(f'Request: {self.request}')
