# Generated by Django 4.2.11 on 2024-05-24 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appShoppee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(),
        ),
    ]