import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

app = Celery('django_app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'redis://localhost:6379'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from app.tasks import (
        add_debt,
        reduce_debt
    )
    # Every 3 hours
    sender.add_periodic_task(3 * 60 * 60, add_debt.s())

    # Executes every day morning at 6:30 a.m.
    sender.add_periodic_task(
        crontab(hour=6, minute=30),
        reduce_debt.s()
    )
