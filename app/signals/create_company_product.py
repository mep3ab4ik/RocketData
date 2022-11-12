from django.db.models.signals import post_save
from django.dispatch import receiver
from app import models


@receiver(post_save, sender=models.SuppliersProduct)
def post_created_product_into_company(
        instance: models.SuppliersProduct, created: bool, **kwargs
):
    """Добавление продукта к поставщику и покупателю """
    suppliers = models.SuppliersProduct.objects.get(pk=instance.pk).suppler
    company = [suppliers.provider, suppliers.seller]
    if created:
        for com in company:
            if not models.CompanyProducts.objects.filter(company=com, product=instance.product).first():
                models.CompanyProducts.objects.create(
                    company=com,
                    product=instance.product
                )


