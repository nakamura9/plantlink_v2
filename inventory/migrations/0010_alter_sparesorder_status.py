# Generated by Django 3.2.13 on 2022-12-13 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_sparesorder_sparesorderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sparesorder',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='draft', max_length=128, null=True),
        ),
    ]
