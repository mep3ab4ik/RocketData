# Generated by Django 4.1.3 on 2022-11-11 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_county_company_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuppliersProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='app.products')),
                ('suppler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='app.suppliers')),
            ],
            options={
                'verbose_name': 'Product of Supplier',
                'verbose_name_plural': 'Products of Suppliers',
            },
        ),
    ]