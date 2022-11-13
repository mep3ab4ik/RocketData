import random

from django_app.celery import app as celery_app
from django.db import transaction
from app import models


@celery_app.task
def add_debt():
    company = models.Company.objects.all()
    for com in company:
        with transaction.atomic():
            com.debt += round(random.uniform(5, 500), 2)
            com.save()


@celery_app.task
def reduce_debt():
    company = models.Company.objects.all()
    for com in company:
        with transaction.atomic():
            com.debt -= round(random.uniform(100, 1000), 2)
            com.save()

# @celery_app.task
# def clear_the_debt_more_20_positions():
