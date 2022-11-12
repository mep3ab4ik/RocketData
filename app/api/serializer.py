from rest_framework import serializers
from app import models


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Products
        fields = [
            'name',
            'model',
            'release_data',
        ]


class CompanySerializer(serializers.ModelSerializer):
    type_company = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    # product = CreateProductSerializer(many=True, read_only=True, required=False)

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
        serializer = CreateProductSerializer(product, many=True)
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


