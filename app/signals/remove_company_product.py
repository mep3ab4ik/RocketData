from django.db.models.signals import pre_delete
from django.dispatch import receiver
from app import models


@receiver(pre_delete, sender=models.CompanyProducts)
def delete_once_product_into_company(instance: models.CompanyProducts, **kwargs):
    """Удаляет продукт в таблице поставщика, когда он удален самой компанией"""

    suppliers_product = models.SuppliersProduct.objects.filter(
        product=instance.product, suppler__provider=instance.company
    ).first()
    if suppliers_product:
        suppliers_product.delete()
