from datetime import datetime
from typing import Optional
from decimal import Decimal

from app import models

from django.db.models import Avg


def avg_debt() -> Decimal:
    company = models.Company.objects
    debt_dict: dict = company.aggregate(avg=Avg('debt'))
    avg: Decimal = Decimal(round(debt_dict.get('avg'), 2))
    return avg


class ValidationCheck:

    @staticmethod
    def valid_name(name: str | None, number: int) -> Optional[str]:
        if not name:
            return '404 :Имя не может быть пустым'
        if len(name) > number:
            return f'404: Имя не может быть больше {number} символов'

    @staticmethod
    def date(date: str) -> Optional[str]:
        if not date:
            return '404: Дата не может быть пустой'
        date = datetime.strptime(date, "%Y-%m-%d")
        date_now = datetime.utcnow()
        if date > date_now:
            return '404: Будущее еще не наступила. Проверь корректность даты'



