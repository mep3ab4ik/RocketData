from django.contrib.auth.models import User
from django.db import models


class TypeCompany(models.Model):
    type = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Type Company"
        verbose_name_plural = "Type Company's"



class Products(models.Model):
    name = models.CharField(max_length=128)
    model = models.CharField(max_length=64)
    release_data = models.DateField()

    def __str__(self):
        return f'{self.name} {self.model}'

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Company(models.Model):
    name = models.CharField(max_length=256, unique=True)
    type_company = models.ForeignKey(TypeCompany, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=64)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    street = models.CharField(max_length=64)
    house_number = models.CharField(max_length=16)
    supplier = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True)
    debt = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.country = self.country.lower()
        self.city = self.city.lower()
        self.street = self.street.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company's"


class CompanyStaff(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_staff')
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff')

    def __str__(self):
        return self.company.name

    class Meta:
        verbose_name_plural = "Company Staff"


class CompanyProducts(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products_company')
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, related_name='company_product')

    def __str__(self):
        return self.product.name

    class Meta:
        unique_together = (('company', 'product'),)
        verbose_name_plural = "Company Products"


class Suppliers(models.Model):
    class Meta:
        unique_together = (('provider', 'seller'),)
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    provider = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='provider')
    seller = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='seller')
    price = models.DecimalField(max_digits=11, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.price < 0:
            self.price = self.price * -1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.provider} - {self.seller}'


class SuppliersProduct(models.Model):
    suppler = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='supplier')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product')

    class Meta:
        unique_together = (('suppler', 'product'),)
        verbose_name = "Product of Supplier"
        verbose_name_plural = "Products of Suppliers"
