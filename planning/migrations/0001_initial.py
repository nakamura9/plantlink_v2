# Generated by Django 3.2.13 on 2022-12-06 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_number', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=64)),
                ('quantity', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('manufacture_date', models.DateField()),
                ('flute_profile', models.CharField(choices=[('a', 'A Flute'), ('b', 'B Flute'), ('c', 'C Flute')], max_length=1)),
                ('liner', models.CharField(choices=[('kraft', 'Kraft')], max_length=32)),
                ('layers', models.IntegerField(choices=[(1, 'Single Wall Board'), (2, 'Double Wall Board')])),
                ('delivery_date', models.DateField()),
                ('customer', models.CharField(max_length=32)),
                ('production_status', models.CharField(choices=[('planned', 'Planned'), ('ongoing', 'Ongoing'), ('completed', 'Completed')], max_length=32)),
                ('delivery_status', models.CharField(choices=[('storage', 'In Storage'), ('transit', 'In Transit'), ('delivered', 'Delivered')], max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RunPlanItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('run_hours', models.FloatField()),
                ('monday', models.BooleanField(default=False)),
                ('tuesday', models.BooleanField(default=False)),
                ('wednesday', models.BooleanField(default=False)),
                ('thursday', models.BooleanField(default=False)),
                ('friday', models.BooleanField(default=False)),
                ('saturday', models.BooleanField(default=False)),
                ('sunday', models.BooleanField(default=False)),
                ('orders', models.ManyToManyField(to='planning.Order')),
            ],
            options={
                'verbose_name': 'Run Schedule',
            },
        ),
    ]