from decimal import Decimal
from typing import Optional

from rest_framework import serializers

from app import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Products
        fields = [
            'id',
            'name',
            'model',
            'release_data',
        ]
        read_only_fields = ['id']


class CompanySerializer(serializers.ModelSerializer):
    type_company = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = models.Company
        fields = [
            'id',
            'name',
            'type_company',
            'supplier',
            'email',
            'country',
            'city',
            'street',
            'house_number',
            'products',
            'debt',
            'created_at',
        ]
        read_only_fields = ['id', 'debt', 'created_at']

    @staticmethod
    def get_type_company(obj: models.Company):
        return obj.type_company.type

    @staticmethod
    def get_supplier(obj: models.Company):
        supplier = obj.supplier
        if supplier:
            return supplier.name

    @staticmethod
    def get_products(obj: models.Company):
        q = []
        for i in obj.products_company.all():
            q.append(i.product.pk)
        product = models.Products.objects.filter(pk__in=q)
        serializer = ProductSerializer(product, many=True)
        return serializer.data


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = [
            'name',
            'type_company',
            'supplier',
            'email',
            'country',
            'city',
            'street',
            'house_number',
        ]


class DebtMoreAvgSerializer(serializers.ModelSerializer):
    avg_debt = serializers.SerializerMethodField()
    company = CompanySerializer(many=True, read_only=True)

    class Meta:
        model = models.Company
        fields = ['avg_debt', 'company']

    @staticmethod
    def get_avg_debt(obj: models.Company) -> Optional[Decimal]:
        return


class UpdateCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Company
        fields = [
            'id',
            'name',
            'type_company',
            'supplier',
            'email',
            'country',
            'city',
            'street',
            'house_number',
            'debt',
            'created_at',
        ]
        read_only_fields = ['id', 'debt', 'created_at']
