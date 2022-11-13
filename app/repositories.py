from app import models

from django.db.models import Avg
from decimal import Decimal


def avg_debt() -> Decimal:
    company = models.Company.objects
    debt_dict: dict = company.aggregate(avg=Avg('debt'))
    avg: Decimal = Decimal(round(debt_dict.get('avg'), 2))
    return avg
