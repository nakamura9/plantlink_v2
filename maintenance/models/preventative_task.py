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


class PreventativeTask(BaseModel):
    """
    Model representing preventatitve maintenance jobs.

    May be once off or recurring 
    Fields: machine, section, subunit, subassembly, component,
            description, tasks, frequency, scheduled_for, estimated_labour_time,assignments, feedback, actual_downtime,completed_date, spares_issued, spares_returned

    Properties: is_open-> Boolean
    """

    dashboard_template = "maintenance/approval.html"
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
    status = models.CharField(max_length=16, choices=[
                            ("requested", "Requested"),
                        ("accepted", "Accepted"),
                        ("completed", "Completed"),
                        ("approved", "Approved"),
                        ("declined", "Declined"),
    ], default="requested")
    

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