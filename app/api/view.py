from decimal import Decimal

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg

from rest_framework import generics
from rest_framework.response import Response

from app.api import serializer
from app import models


class CompanyView(generics.ListAPIView):
    """
    Информация обо все объектах сети, где есть авторизированный сотрудник
    """
    serializer_class = serializer.CompanySerializer
    queryset = models.Company.objects

    def get(self, request, *args, **kwargs) -> Response:
        queryset = self.queryset.filter(company_staff__staff=request.user.pk)
        serializers = serializer.CompanySerializer(queryset, many=True)
        return Response(serializers.data)


class CountyCompanyView(generics.ListAPIView):
    """
    Информацию об объектах определённой страны(фильтр на названию страны)
    """
    serializer_class = serializer.CompanySerializer
    queryset = models.Company.objects

    def get(self, request, country: str, *args, **kwargs) -> Response:
        queryset = self.queryset.filter(company_staff__staff=request.user.pk, country=country.lower())
        serializers = serializer.CompanySerializer(queryset, many=True)
        return Response(serializers.data)


class CreateCompanyView(generics.CreateAPIView):
    """
    Создать новую запить об объекте сети
    """
    serializer_class = serializer.CreateCompanySerializer

    def post(self, request, *args, **kwargs) -> HttpResponse:
        company = models.Company()

        type_company = models.TypeCompany.objects.filter(pk=request.data.get('type_company', None)).first()

        company.name = request.data.get('name', None)
        company.type_company = type_company
        company.email = request.data.get('email', None)
        company.country = request.data.get('country', None)
        company.city = request.data.get('city', None)
        company.street = request.data.get('street', None)
        company.house_number = request.data.get('house_number', None)
        company.supplier = request.data.get('supplier', None)
        company.save()
        return HttpResponse("201: Cоздана новая запись об объекте сети")


class RemoveCompanyView(generics.DestroyAPIView):

    def delete(self, request, pk: int,  *args, **kwargs) -> HttpResponse:
        try:
            company = models.Company.objects.get(pk=pk)
            company.delete()
            return HttpResponse('204: Запись об объекте сети была удалена')
        except ObjectDoesNotExist:
            return HttpResponse('404: Объект сети не найден/не существует')


class CreateProductsView(generics.CreateAPIView):
    """
    Создать новую запить об продукте
    """
    serializer_class = serializer.CreateProductSerializer

    def post(self, request, *args, **kwargs) -> HttpResponse:
        products = models.Products()

        products.name = request.data.get('name', None)
        products.model = request.data.get('model', None)
        products.release_data = request.data.get('release_data', None)
        products.save()
        return HttpResponse("201: Cоздана новая запись об продукте")


class RemoveProductsView(generics.DestroyAPIView):
    """
    Удалить запись продукта
    """
    def delete(self, request, pk: int,  *args, **kwargs) -> HttpResponse:
        try:
            company = models.Products.objects.get(pk=pk)
            company.delete()
            return HttpResponse('204: Запись об продукте была удалена')
        except ObjectDoesNotExist:
            return HttpResponse('404: Запись продукта не найдена/не существует')


class FindCompanyWithProductView(generics.ListAPIView):
    """
    Все объекты сети, где можно встретить определённый продукт (фильтр по id продкута)
    """

    serializer_class = serializer.CompanySerializer
    queryset = models.Company.objects

    def get(self, request, pk: int, *args, **kwargs) -> Response:
        queryset = self.queryset.filter(company_staff__staff=request.user.pk)
        serializers = serializer.CompanySerializer(queryset, many=True)
        return Response(serializers.data)


class MoreAvgDebtView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        avg_debt: dict = models.Company.objects.aggregate(avg=Avg('debt'))
        avg = Decimal(avg_debt.get('avg'))
        a= models.Company.objects.filter(debt__lt=avg)
        f =1