# Generated by Django 4.2.11 on 2024-05-27 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appShoppee', '0006_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
    ]
