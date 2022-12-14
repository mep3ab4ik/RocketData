# Generated by Django 4.1.3 on 2022-11-14 18:54

from django.db import migrations, transaction


def create_type_company(apps, schema_editor):
    TypeCompany = apps.get_model('app', 'TypeCompany')
    data = ['Завод', 'Дистрибьютор', 'Дилерский центр', 'Крупная розничная сеть', 'Индивидуальный предприниматель']
    for info in data:
        with transaction.atomic():
            TypeCompany.objects.create(type=info)


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_companyproducts_company_and_more'),
    ]

    operations = [
        migrations.RunPython(create_type_company),
    ]
