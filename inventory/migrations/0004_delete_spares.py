# Generated by Django 3.2.13 on 2022-12-06 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20221206_1906'),
        ('maintenance', '0005_auto_20221206_1906'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Spares',
        ),
    ]