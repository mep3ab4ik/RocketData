from decimal import Decimal
from typing import Union

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import views

from rest_framework import generics, status
from rest_framework.response import Response

from app.api import serializer
from app import models
from app.repositories import avg_debt


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

    def post(self, request, *args, **kwargs) -> Response:
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
        return Response(status=status.HTTP_201_CREATED)


class RemoveCompanyView(generics.DestroyAPIView):

    def delete(self, request, pk: int, *args, **kwargs) -> Union[Response, ObjectDoesNotExist]:
        try:
            company = models.Company.objects.get(pk=pk)
            company.delete()
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateProductsView(generics.CreateAPIView):
    """
    Создать новую запить об продукте
    """
    serializer_class = serializer.ProductSerializer

    def post(self, request, *args, **kwargs) -> Response:
        products = models.Products()

        products.name = request.data.get('name', None)
        products.model = request.data.get('model', None)
        products.release_data = request.data.get('release_data', None)
        products.save()
        return Response(status=status.HTTP_201_CREATED)


class RemoveProductsView(generics.DestroyAPIView):
    """
    Удалить запись продукта
    """

    def delete(self, request, pk: int, *args, **kwargs) -> Union[Response, ObjectDoesNotExist]:
        try:
            company = models.Products.objects.get(pk=pk)
            company.delete()
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FindCompanyWithProductView(generics.ListAPIView):
    """
    Все объекты сети, где можно встретить определённый продукт (фильтр по id продкута)
    """

    serializer_class = serializer.CompanySerializer
    queryset = models.Company.objects

    def get(self, request, pk: int, *args, **kwargs) -> Response:
        queryset = self.queryset.filter(company_staff__staff=request.user.pk, products_company__product=pk)
        serializers = serializer.CompanySerializer(queryset, many=True)
        return Response(serializers.data)


class MoreAvgDebtView(generics.ListAPIView):
    """
    Выводит среднею задолженность по объектам сети и сами объекты, где задолженность превышает среднею
    """
    serializer_class = serializer.DebtMoreAvgSerializer
    queryset = models.Company.objects

    def get(self, request, *args, **kwargs) -> Response:
        static = {
            'avg_debt': None,
            'company': None,
        }
        avg: Decimal = avg_debt()
        static['avg_debt'] = avg
        queryset = self.queryset.filter(company_staff__staff=request.user.pk, debt__gt=avg)
        static['company'] = serializer.CompanySerializer(queryset, many=True).data
        return Response(static, status=status.HTTP_200_OK)


class UpdateProductView(views.APIView):
    """
    Обновление информации об продукте
    """
    serializer_class = serializer.ProductSerializer

    def patch(self, request, pk: int, *args, **kwargs) -> Union[Response, ObjectDoesNotExist]:
        try:
            product = models.Products.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.name = request.data.get('name', None)
        product.model = request.data.get('model', None)
        product.release_data = request.data.get('release_data', None)
        product.save()
        return Response(status=status.HTTP_200_OK)


class UpdateCompanyView(views.APIView):
    """
    Обновление информации об объекте сети
    """
    serializer_class = serializer.UpdateCompanySerializer

    def patch(self, request, pk: int, *args, **kwargs) -> Union[Response, HttpResponse, ObjectDoesNotExist]:

        try:
            company = models.Company.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            type_company = models.TypeCompany.objects.get(pk=request.data.get('type_company'))
        except ObjectDoesNotExist:
            return HttpResponse('Такого типа компании не суще')

        try:
            supplier = models.Company.objects.get(pk=request.data.get('supplier'))
        except ObjectDoesNotExist:
            return HttpResponse('Такого поставщика не существует ')

        company.name = request.data.get('name', None)
        company.email = request.data.get('email', None)
        company.type_company = type_company
        company.country = request.data.get('country', None)
        company.city = request.data.get('city', None)
        company.street = request.data.get('street', None)
        company.house_number = request.data.get('house_number', None)
        company.supplier = supplier
        company.save()
        return Response(status=status.HTTP_200_OK)
