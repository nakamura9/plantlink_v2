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
        'resolver_action',
        'actual_labour_time',
        'downtime',
        'completion_date',
        'section_break',
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
    assigned_to = models.ForeignKey("base.Account", on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=4,
                                choices=[("high", "High"), ("low", "Low")])
    status = models.CharField(max_length=16, choices=[
                            ("requested", "Requested"),
                        ("accepted", "Accepted"),
                        ("completed", "Completed"),
                        ("approved", "Approved"),
                        ("declined", "Declined"),
    ], default="requested")

    resolver_action= models.TextField(null=True, blank=True)
    actual_labour_time = models.DurationField(null=True, choices=time_duration, blank=True)
    downtime = models.DurationField(null=True, choices=time_duration, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    spares_issued = models.ManyToManyField("inventory.Item", related_name="%(class)s_spares_issued", blank=True)
    spares_returned = models.ManyToManyField("inventory.Item",related_name="%(class)s_spares_returned", blank=True)
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
