# Generated by Django 3.2.13 on 2022-04-25 12:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Costing',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=32, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='PreventativeTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('frequency', models.CharField(choices=[('once', 'Once off'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('fortnightly', 'Every 2 weeks'), ('monthly', 'Monthly'), ('quarterly', 'Every 3 Months'), ('bi-annually', 'Every 6 Months'), ('yearly', 'Yearly')], max_length=16)),
                ('estimated_labour_time', models.DurationField(choices=[(datetime.timedelta(0, 300), '00:05'), (datetime.timedelta(0, 600), '00:10'), (datetime.timedelta(0, 900), '00:15'), (datetime.timedelta(0, 1200), '00:20'), (datetime.timedelta(0, 1500), '00:25'), (datetime.timedelta(0, 1800), '00:30'), (datetime.timedelta(0, 2700), '00:45'), (datetime.timedelta(0, 3600), '01:00'), (datetime.timedelta(0, 4500), '01:15'), (datetime.timedelta(0, 5400), '01:30'), (datetime.timedelta(0, 6300), '01:45'), (datetime.timedelta(0, 7200), '02:00'), (datetime.timedelta(0, 10800), '03:00'), (datetime.timedelta(0, 14400), '04:00'), (datetime.timedelta(0, 18000), '05:00'), (datetime.timedelta(0, 21600), '06:00'), (datetime.timedelta(0, 25200), '07:00'), (datetime.timedelta(0, 28800), '08:00'), (datetime.timedelta(0, 32400), '09:00'), (datetime.timedelta(0, 36000), '10:00'), (datetime.timedelta(0, 39600), '11:00'), (datetime.timedelta(0, 43200), '12:00'), (datetime.timedelta(0, 46800), '13:00'), (datetime.timedelta(0, 50400), '14:00'), (datetime.timedelta(0, 54000), '15:00'), (datetime.timedelta(0, 57600), '16:00'), (datetime.timedelta(0, 61200), '17:00'), (datetime.timedelta(0, 64800), '18:00'), (datetime.timedelta(0, 68400), '19:00'), (datetime.timedelta(0, 72000), '20:00'), (datetime.timedelta(0, 75600), '21:00'), (datetime.timedelta(0, 79200), '22:00')])),
                ('estimated_downtime', models.DurationField(choices=[(datetime.timedelta(0, 300), '00:05'), (datetime.timedelta(0, 600), '00:10'), (datetime.timedelta(0, 900), '00:15'), (datetime.timedelta(0, 1200), '00:20'), (datetime.timedelta(0, 1500), '00:25'), (datetime.timedelta(0, 1800), '00:30'), (datetime.timedelta(0, 2700), '00:45'), (datetime.timedelta(0, 3600), '01:00'), (datetime.timedelta(0, 4500), '01:15'), (datetime.timedelta(0, 5400), '01:30'), (datetime.timedelta(0, 6300), '01:45'), (datetime.timedelta(0, 7200), '02:00'), (datetime.timedelta(0, 10800), '03:00'), (datetime.timedelta(0, 14400), '04:00'), (datetime.timedelta(0, 18000), '05:00'), (datetime.timedelta(0, 21600), '06:00'), (datetime.timedelta(0, 25200), '07:00'), (datetime.timedelta(0, 28800), '08:00'), (datetime.timedelta(0, 32400), '09:00'), (datetime.timedelta(0, 36000), '10:00'), (datetime.timedelta(0, 39600), '11:00'), (datetime.timedelta(0, 43200), '12:00'), (datetime.timedelta(0, 46800), '13:00'), (datetime.timedelta(0, 50400), '14:00'), (datetime.timedelta(0, 54000), '15:00'), (datetime.timedelta(0, 57600), '16:00'), (datetime.timedelta(0, 61200), '17:00'), (datetime.timedelta(0, 64800), '18:00'), (datetime.timedelta(0, 68400), '19:00'), (datetime.timedelta(0, 72000), '20:00'), (datetime.timedelta(0, 75600), '21:00'), (datetime.timedelta(0, 79200), '22:00')])),
                ('scheduled_for', models.DateField()),
                ('feedback', models.TextField(null=True)),
                ('actual_downtime', models.DurationField(choices=[(datetime.timedelta(0, 300), '00:05'), (datetime.timedelta(0, 600), '00:10'), (datetime.timedelta(0, 900), '00:15'), (datetime.timedelta(0, 1200), '00:20'), (datetime.timedelta(0, 1500), '00:25'), (datetime.timedelta(0, 1800), '00:30'), (datetime.timedelta(0, 2700), '00:45'), (datetime.timedelta(0, 3600), '01:00'), (datetime.timedelta(0, 4500), '01:15'), (datetime.timedelta(0, 5400), '01:30'), (datetime.timedelta(0, 6300), '01:45'), (datetime.timedelta(0, 7200), '02:00'), (datetime.timedelta(0, 10800), '03:00'), (datetime.timedelta(0, 14400), '04:00'), (datetime.timedelta(0, 18000), '05:00'), (datetime.timedelta(0, 21600), '06:00'), (datetime.timedelta(0, 25200), '07:00'), (datetime.timedelta(0, 28800), '08:00'), (datetime.timedelta(0, 32400), '09:00'), (datetime.timedelta(0, 36000), '10:00'), (datetime.timedelta(0, 39600), '11:00'), (datetime.timedelta(0, 43200), '12:00'), (datetime.timedelta(0, 46800), '13:00'), (datetime.timedelta(0, 50400), '14:00'), (datetime.timedelta(0, 54000), '15:00'), (datetime.timedelta(0, 57600), '16:00'), (datetime.timedelta(0, 61200), '17:00'), (datetime.timedelta(0, 64800), '18:00'), (datetime.timedelta(0, 68400), '19:00'), (datetime.timedelta(0, 72000), '20:00'), (datetime.timedelta(0, 75600), '21:00'), (datetime.timedelta(0, 79200), '22:00')], null=True)),
                ('completed_date', models.DateField(null=True)),
                ('comments', models.TextField(null=True)),
                ('assignments', models.ManyToManyField(related_name='preventativetask_assignments_made', to='base.Account')),
                ('assignments_accepted', models.ManyToManyField(related_name='preventativetask_assignments_accepted', to='base.Account')),
                ('component', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.component')),
                ('machine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.machine')),
                ('required_spares', models.ManyToManyField(related_name='preventativetask_required_spares', to='inventory.Spares')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.section')),
                ('spares_used', models.ManyToManyField(related_name='preventativetask_spares_used', to='inventory.Spares')),
                ('subassembly', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.subassembly')),
                ('subunit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.subunit')),
                ('tasks', models.ManyToManyField(to='base.Task')),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('execution_date', models.DateField(default=datetime.date.today)),
                ('estimated_labour_time', models.DurationField(choices=[(datetime.timedelta(0, 300), '00:05'), (datetime.timedelta(0, 600), '00:10'), (datetime.timedelta(0, 900), '00:15'), (datetime.timedelta(0, 1200), '00:20'), (datetime.timedelta(0, 1500), '00:25'), (datetime.timedelta(0, 1800), '00:30'), (datetime.timedelta(0, 2700), '00:45'), (datetime.timedelta(0, 3600), '01:00'), (datetime.timedelta(0, 4500), '01:15'), (datetime.timedelta(0, 5400), '01:30'), (datetime.timedelta(0, 6300), '01:45'), (datetime.timedelta(0, 7200), '02:00'), (datetime.timedelta(0, 10800), '03:00'), (datetime.timedelta(0, 14400), '04:00'), (datetime.timedelta(0, 18000), '05:00'), (datetime.timedelta(0, 21600), '06:00'), (datetime.timedelta(0, 25200), '07:00'), (datetime.timedelta(0, 28800), '08:00'), (datetime.timedelta(0, 32400), '09:00'), (datetime.timedelta(0, 36000), '10:00'), (datetime.timedelta(0, 39600), '11:00'), (datetime.timedelta(0, 43200), '12:00'), (datetime.timedelta(0, 46800), '13:00'), (datetime.timedelta(0, 50400), '14:00'), (datetime.timedelta(0, 54000), '15:00'), (datetime.timedelta(0, 57600), '16:00'), (datetime.timedelta(0, 61200), '17:00'), (datetime.timedelta(0, 64800), '18:00'), (datetime.timedelta(0, 68400), '19:00'), (datetime.timedelta(0, 72000), '20:00'), (datetime.timedelta(0, 75600), '21:00'), (datetime.timedelta(0, 79200), '22:00')])),
                ('priority', models.CharField(choices=[('high', 'High'), ('low', 'Low')], max_length=4)),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('completed', 'Completed'), ('approved', 'Approved'), ('declined', 'Declined')], default='requested', max_length=16)),
                ('resolver_action', models.TextField(null=True)),
                ('actual_labour_time', models.DurationField(choices=[(datetime.timedelta(0, 300), '00:05'), (datetime.timedelta(0, 600), '00:10'), (datetime.timedelta(0, 900), '00:15'), (datetime.timedelta(0, 1200), '00:20'), (datetime.timedelta(0, 1500), '00:25'), (datetime.timedelta(0, 1800), '00:30'), (datetime.timedelta(0, 2700), '00:45'), (datetime.timedelta(0, 3600), '01:00'), (datetime.timedelta(0, 4500), '01:15'), (datetime.timedelta(0, 5400), '01:30'), (datetime.timedelta(0, 6300), '01:45'), (datetime.timedelta(0, 7200), '02:00'), (datetime.timedelta(0, 10800), '03:00'), (datetime.timedelta(0, 14400), '04:00'), (datetime.timedelta(0, 18000), '05:00'), (datetime.timedelta(0, 21600), '06:00'), (datetime.timedelta(0, 25200), '07:00'), (datetime.timedelta(0, 28800), '08:00'), (datetime.timedelta(0, 32400), '09:00'), (datetime.timedelta(0, 36000), '10:00'), (datetime.timedelta(0, 39600), '11:00'), (datetime.timedelta(0, 43200), '12:00'), (datetime.timedelta(0, 46800), '13:00'), (datetime.timedelta(0, 50400), '14:00'), (datetime.timedelta(0, 54000), '15:00'), (datetime.timedelta(0, 57600), '16:00'), (datetime.timedelta(0, 61200), '17:00'), (datetime.timedelta(0, 64800), '18:00'), (datetime.timedelta(0, 68400), '19:00'), (datetime.timedelta(0, 72000), '20:00'), (datetime.timedelta(0, 75600), '21:00'), (datetime.timedelta(0, 79200), '22:00')], null=True)),
                ('downtime', models.DurationField(choices=[(datetime.timedelta(0, 300), '00:05'), (datetime.timedelta(0, 600), '00:10'), (datetime.timedelta(0, 900), '00:15'), (datetime.timedelta(0, 1200), '00:20'), (datetime.timedelta(0, 1500), '00:25'), (datetime.timedelta(0, 1800), '00:30'), (datetime.timedelta(0, 2700), '00:45'), (datetime.timedelta(0, 3600), '01:00'), (datetime.timedelta(0, 4500), '01:15'), (datetime.timedelta(0, 5400), '01:30'), (datetime.timedelta(0, 6300), '01:45'), (datetime.timedelta(0, 7200), '02:00'), (datetime.timedelta(0, 10800), '03:00'), (datetime.timedelta(0, 14400), '04:00'), (datetime.timedelta(0, 18000), '05:00'), (datetime.timedelta(0, 21600), '06:00'), (datetime.timedelta(0, 25200), '07:00'), (datetime.timedelta(0, 28800), '08:00'), (datetime.timedelta(0, 32400), '09:00'), (datetime.timedelta(0, 36000), '10:00'), (datetime.timedelta(0, 39600), '11:00'), (datetime.timedelta(0, 43200), '12:00'), (datetime.timedelta(0, 46800), '13:00'), (datetime.timedelta(0, 50400), '14:00'), (datetime.timedelta(0, 54000), '15:00'), (datetime.timedelta(0, 57600), '16:00'), (datetime.timedelta(0, 61200), '17:00'), (datetime.timedelta(0, 64800), '18:00'), (datetime.timedelta(0, 68400), '19:00'), (datetime.timedelta(0, 72000), '20:00'), (datetime.timedelta(0, 75600), '21:00'), (datetime.timedelta(0, 79200), '22:00')], null=True)),
                ('completion_date', models.DateField(null=True)),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.account')),
                ('comments', models.ManyToManyField(to='base.Comment')),
                ('component', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.component')),
                ('costing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maintenance.costing')),
                ('machine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.machine')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.section')),
                ('spares_issued', models.ManyToManyField(related_name='workorder_spares_issued', to='inventory.Spares')),
                ('spares_returned', models.ManyToManyField(related_name='workorder_spares_returned', to='inventory.Spares')),
                ('subassembly', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.subassembly')),
                ('subunit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.subunit')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.category')),
            ],
        ),
        migrations.CreateModel(
            name='SparesRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('unit', models.CharField(blank=True, max_length=32, null=True)),
                ('quantity', models.FloatField(default=0.0)),
                ('linked_spares', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.spares')),
                ('preventative_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maintenance.preventativetask')),
            ],
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('creation_date', models.DateField()),
                ('last_completed_date', models.DateField(blank=True, null=True)),
                ('estimated_time', models.DurationField(choices=[(datetime.timedelta(0, 300), '00:05'), (datetime.timedelta(0, 600), '00:10'), (datetime.timedelta(0, 900), '00:15'), (datetime.timedelta(0, 1200), '00:20'), (datetime.timedelta(0, 1500), '00:25'), (datetime.timedelta(0, 1800), '00:30'), (datetime.timedelta(0, 3600), '01:00'), (datetime.timedelta(0, 7200), '02:00'), (datetime.timedelta(0, 10800), '03:00'), (datetime.timedelta(0, 14400), '04:00'), (datetime.timedelta(0, 18000), '05:00'), (datetime.timedelta(0, 21600), '06:00'), (datetime.timedelta(0, 25200), '07:00'), (datetime.timedelta(0, 28800), '08:00')])),
                ('start_time', models.TimeField(choices=[(datetime.time(6, 30), '06:30'), (datetime.time(7, 0), '07:00'), (datetime.time(7, 30), '07:30'), (datetime.time(8, 0), '08:00'), (datetime.time(8, 30), '08:30'), (datetime.time(9, 0), '09:00'), (datetime.time(9, 30), '09:30'), (datetime.time(10, 0), '10:00'), (datetime.time(10, 30), '10:30'), (datetime.time(11, 0), '11:00'), (datetime.time(11, 30), '11:30'), (datetime.time(12, 0), '12:00'), (datetime.time(12, 30), '12:30'), (datetime.time(13, 0), '13:00'), (datetime.time(13, 30), '13:30'), (datetime.time(14, 0), '14:00'), (datetime.time(14, 30), '14:30'), (datetime.time(15, 0), '15:00'), (datetime.time(15, 30), '15:30'), (datetime.time(16, 0), '16:00'), (datetime.time(16, 30), '16:30'), (datetime.time(17, 0), '17:00')])),
                ('category', models.CharField(choices=[('electrical', 'Electrical'), ('mechanical', 'Mechanical')], max_length=64)),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('fortnightly', 'Every 2 weeks'), ('monthly', 'Monthly'), ('quarterly', 'Every 3 Months'), ('bi-annually', 'Every 6 Months'), ('yearly', 'Yearly')], max_length=16)),
                ('on_hold', models.BooleanField(default=False)),
                ('comments', models.ManyToManyField(to='base.Comment')),
                ('component', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.component')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.machine')),
                ('resolver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.account')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.section')),
                ('subassembly', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.subassembly')),
                ('subunit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.subunit')),
                ('tasks', models.ManyToManyField(to='base.Task')),
            ],
        ),
    ]
