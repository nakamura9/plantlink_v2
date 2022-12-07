from __future__ import unicode_literals
import time
import datetime
from itertools import chain

from django.utils import timezone
from django.db import models
from django.db.models import Q

from inventory.models import *
from base.models import BaseModel
from base.utilities import time_choices


time_duration = [] + time_choices("00:05:00", "00:30:00", "00:05:00",
            delta=True) + time_choices("00:30:00", "02:00:00", "00:15:00",
            delta=True) + time_choices("02:00:00", "23:00:00", "01:00:00",
            delta=True)


class WorkOrder(BaseModel):
    """
    Model that represents a job assigned ad-hoc i.e. a breakdown.
    """

    list_fields = ['machine', 'assigned_to', 'status']
    dashboard_template = "maintenance/approval.html"
    read_only_fields = [
        'assigned_to', 'machine', 'section', 
        'subunit', 'subassembly', 'component', 
        'estimated_labour_time', 'status', 'priority',
        'description', 'execution_date'
        ]
    filter_fields = {
        'machine': ['exact'],
        'assigned_to': ['exact'],
        'status': ['exact'],
        'execution_date': ['gte', 'lte']
    }
    field_order = [
        'description',
        'execution_date',
        'estimated_labour_time',
        'assigned_to',
        'priority',
        'column_break',
        'machine',
        'section',
        'subunit',
        'subassembly',
        'component',
        'column_break',
        'status',
        'resolver_action',
        'actual_labour_time',
        'downtime',
        'completion_date',
        'section_break',
        'spares_issued',
        'spares_returned',
        'column_break',
        'comments'
    ]

    machine = models.ForeignKey("inventory.Machine", null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey("inventory.Section", null=True, on_delete=models.SET_NULL)
    subunit = models.ForeignKey("inventory.SubUnit", null=True, blank=True, on_delete=models.SET_NULL)
    subassembly = models.ForeignKey("inventory.SubAssembly", null=True, blank=True, on_delete=models.SET_NULL)
    component = models.ForeignKey("inventory.Component", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(unique=False)
    execution_date = models.DateField(default=datetime.date.today)
    estimated_labour_time = models.DurationField(choices = time_duration)
    assigned_to = models.ForeignKey("base.Account", on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=4,
                                choices=[("high", "High"), ("low", "Low")])
    status = models.CharField(max_length=16, choices=[
                            ("requested", "Requested"),
                        ("accepted", "Accepted"),
                        ("completed", "Completed"),
                        ("approved", "Approved"),
                        ("declined", "Declined"),
    ], default="requested")

    resolver_action= models.TextField(null=True)
    actual_labour_time = models.DurationField(null=True, choices=time_duration)
    downtime = models.DurationField(null=True, choices=time_duration)
    completion_date = models.DateField(null=True, blank=True)
    spares_issued = models.ManyToManyField("inventory.Item", related_name="%(class)s_spares_issued")
    spares_returned = models.ManyToManyField("inventory.Item",related_name="%(class)s_spares_returned")
    comments = models.TextField(blank=True, default="")

    @property
    def is_open(self):
        return self.status == "requested" or self.status == "accepted"

    @property
    def downtime_hours(self):
        if not self.downtime:
            return 0

        return self.downtime.seconds / 3600.0

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = "requested"
        obj = super(WorkOrder, self).save(*args, **kwargs)
        net_spares = [sp for sp in self.spares_issued.all() if sp not in \
                            self.spares_returned.all()]
        if self.component:
            for s in net_spares:
                self.component.spares_data.add(s) 

        return obj

    def __str__(self):
        return f"WO-{'%06d' % self.pk}"


class PreventativeTask(BaseModel):
    """
    Model representing preventatitve maintenance jobs.

    May be once off or recurring 
    Fields: machine, section, subunit, subassembly, component,
            description, tasks, frequency, scheduled_for, estimated_labour_time,assignments, feedback, actual_downtime,completed_date, spares_issued, spares_returned

    Properties: is_open-> Boolean
    """

    list_fields = ['machine', 'section', 'estimated_downtime']
    read_only_fields = [
        'description', 'estimated_labour_time', 'estimated_downtime', 'scheduled_for',
        'frequency', 'assignments', 'required_spares', 'machine', 'section',
        'subunit', 'subassembly', 'component'

    ]
    filter_fields = {
        'machine': ['exact'],
    }
    
    field_order = [
        'description',
        'frequency',
        'estimated_labour_time',
        'estimated_downtime',
        'assignments',
        'scheduled_for',
        'required_spares',
        'column_break',
        'machine',
        'section',
        'subunit',
        'subassembly',
        'component',
        'column_break',
        'completed_date',
        'actual_downtime',
        'assignments_accepted',
        'feedback',        
        'spares_used',
        'comments'
    ]
    
    mapping =  {"daily": 1,
        "weekly": 7,
        "fortnightly": 14,
        "monthly": 30,
        "quarterly": 90,
        "bi-annually": 180,
        "yearly": 360}

    machine = models.ForeignKey("inventory.Machine", null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey("inventory.Section", null=True, blank=True, on_delete=models.SET_NULL)
    subunit = models.ForeignKey("inventory.SubUnit", null=True, blank=True, on_delete=models.SET_NULL)
    subassembly = models.ForeignKey("inventory.SubAssembly", null=True, blank=True, on_delete=models.SET_NULL)
    component = models.ForeignKey("inventory.Component", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(unique=False)
    frequency = models.CharField(max_length = 16, 
                        choices = [("once", "Once off"),
                                    ("daily", "Daily"),
                                    ("weekly", "Weekly"),
                                    ("fortnightly", "Every 2 weeks"),
                                    ("monthly", "Monthly"),
                                    ("quarterly", "Every 3 Months"),
                                    ("bi-annually", "Every 6 Months"), 
                                    ("yearly", "Yearly")])

    estimated_labour_time = models.DurationField(choices=time_duration)
    estimated_downtime = models.DurationField(choices=time_duration)
    scheduled_for = models.DateField()
    required_spares = models.ManyToManyField("inventory.Item", related_name="%(class)s_required_spares", blank=True)
    assignments = models.ManyToManyField("base.Account", related_name="%(class)s_assignments_made", blank=True)
    assignments_accepted = models.ManyToManyField("base.Account", related_name="%(class)s_assignments_accepted", blank=True)
    feedback = models.TextField(null=True, blank=True)
    actual_downtime = models.DurationField(null=True,choices=time_duration, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    spares_used = models.ManyToManyField("inventory.Item", related_name="%(class)s_spares_used", blank=True)
    comments  = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return f"PT-{'%06d' % self.pk }"

    @property
    def outstanding_responses(self):
        return list(chain([a for a in self.assignments.all() if a not in self.assignments_accepted.all()]))

    @property
    def is_open(self):
        if self.completed_date is None:
            return True
        else:
            if self.frequency == "once":
                return False
            
            delta = datetime.date.today() - self.completed_date

        if delta.days > self.mapping[self.frequency]:
            return True
        else:
            return False

class PreventativeMaintenanceItem(models.Model):
    parent = models.ForeignKey('maintenance.preventativetask', on_delete=models.CASCADE)
    description = models.TextField()

class SparesRequest(BaseModel):
    list_fields = ['preventative_task','date', 'name']
    filter_fields = {
        'date': ['exact'],
        'preventative_task': ['exact'],
    }
    field_order = [
        'date',
        'name',
        'column_break',
        'preventative_task',
        'requested_by',
        'section_break',
        'child:maintenance.sparesrequestitem'
    ]
    date = models.DateField()
    name = models.CharField(max_length= 32, null=True, blank=True)
    requested_by = models.CharField(max_length= 32, null=True, blank=True)
    preventative_task = models.ForeignKey("PreventativeTask", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "REQ-%06d" % self.pk


class SparesRequestItem(models.Model):
    field_order = ['item', 'unit', 'quantity']

    parent = models.ForeignKey('maintenance.sparesrequest', on_delete=models.CASCADE)
    item = models.ForeignKey("inventory.Item", null=True, on_delete=models.SET_NULL)
    unit = models.CharField(max_length = 32, null=True, blank=True)
    quantity = models.FloatField(default=0.0)