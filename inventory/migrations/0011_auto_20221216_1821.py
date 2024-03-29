# Generated by Django 3.2.13 on 2022-12-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_sparesorder_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='asset',
            name='void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='component',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='component',
            name='void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='machine',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='machine',
            name='void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plant',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plant',
            name='void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='section',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='section',
            name='void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sparesorder',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sparesorder',
            name='void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subassembly',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subassembly',
            name='void',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subunit',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subunit',
            name='void',
            field=models.BooleanField(default=False),
        ),
    ]
