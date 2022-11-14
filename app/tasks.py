import random
from decimal import Decimal

from django_app.celery import app as celery_app
from django.db import transaction
from django.core import mail
from django.conf import settings
import qrcode

from app import models


@celery_app.task(name='add_debt')
def add_debt() -> None:
    company = models.Company.objects.all()
    for com in company:
        with transaction.atomic():
            com.debt += Decimal(round(random.uniform(5, 500), 2))
            com.save()


@celery_app.task(name='reduce_debt')
def reduce_debt() -> None:
    company = models.Company.objects.all()
    for com in company:
        with transaction.atomic():
            com.debt -= Decimal(round(random.uniform(100, 1000), 2))
            com.save()


@celery_app.task(name='clear_the_debt')
def clear_the_debt(queryset: list[int]) -> None:
    queryset = models.Company.objects.filter(pk__in=queryset)
    for company in queryset:
        with transaction.atomic():
            company.debt = Decimal(0)
            company.save()


@celery_app.task(name='send_email')
def send_email(name_company: str, info_company: str, email: str) -> None:
    path = 'media/qr/qrcode.png'
    qr_code = qrcode.make(info_company)
    qr_code.save(path)

    with mail.get_connection() as connection:
        email = mail.EmailMessage(
            subject=f'Ваш запрос контактной информации об объекте {name_company}',
            body=info_company,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            connection=connection,
        )
        email.attach_file(path)
        email.send(fail_silently=False)
