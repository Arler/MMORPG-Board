from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MMORPG_board.settings')

app = Celery('MMORPG_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# crontab(minute='0', hour='20')

app.conf.beat_schedule = {
	'daily_announcements': {
		'task': 'board.tasks.daily_announcements_email',
		'schedule': crontab(minute='0', hour='*/24'),
		'args': (),
	}
}