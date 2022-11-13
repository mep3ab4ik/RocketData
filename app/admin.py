import random

from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext

from app import models


@admin.register(models.TypeCompany)
class TypeCompanyAdmin(admin.ModelAdmin):
    model = models.TypeCompany
    ordering = ['id']
    list_display = ['type']
    fields = ['type']


@admin.register(models.Products)
class ProductsAdmin(admin.ModelAdmin):
    model = models.Products
    ordering = ['id']
    list_display = ['name', 'model', 'release_data']



class CompanyProductsInline(admin.StackedInline):
    model = models.CompanyProducts
    list_display = ['product']
    extra = 1


class CompanyStaffInline(admin.StackedInline):
    model = models.CompanyStaff
    list_display = ['staff']
    extra = 1


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    model = models.Company
    ordering = ['id']
    list_display = ['name', 'type_company', 'created_at']
    list_filter = ['city']
    fields = [
        'name',
        'type_company',
        'country',
        'city',
        'street',
        'house_number',
        'supplier',
        'url_supplier',
        'debt',
        'email',
        'created_at',
    ]
    readonly_fields = ['created_at', 'url_supplier']
    inlines = [CompanyStaffInline, CompanyProductsInline]
    actions = ['clear_debt']
    @staticmethod
    def url_supplier(request):
        if not request.supplier:
            return
        provider = models.Company.objects.filter(supplier=request.supplier).first()
        return mark_safe(
            f'<a href=http://127.0.0.1:8000/admin/app/company/{provider.supplier.pk}/change/>'
            f'{provider.supplier}'
            f'</a>'
        )
    @admin.action(description="Remove debts to suppliers selected Company's'")
    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, ngettext(
            '%d debt was successfully removed.',
            '%d debts were successfully removed.',
            updated,
        ) % updated, messages.SUCCESS)


class SuppliersProductInline(admin.StackedInline):
    model = models.SuppliersProduct
    list_display = ['product']
    extra = 1

@admin.register(models.Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    model = models.Suppliers

    ordering = ['id']
    list_display = ['provider', 'seller', 'price']
    fields = [
        'provider',
        'seller',
        'price',
        'updated_at',
        'created_at'
    ]
    inlines = [SuppliersProductInline]
    readonly_fields = ['updated_at', 'created_at', 'provider']
