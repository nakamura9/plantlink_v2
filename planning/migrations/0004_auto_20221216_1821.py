# Generated by Django 3.2.13 on 2022-12-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0003_alter_runplanitem_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='runplanitem',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='runplanitem',
            name='void',
            field=models.BooleanField(default=False),
        ),
    ]
