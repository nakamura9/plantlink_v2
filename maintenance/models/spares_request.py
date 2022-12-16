from __future__ import unicode_literals

from django.db import models

from inventory.models import *
from base.models import BaseModel
from base.utilities import time_choices


class SparesRequest(BaseModel):
    dashboard_template = "maintenance/spares_request_approval.html"
    list_fields = ['requested_by','date', 'request_type', 'status']
    can_submit = True
    filter_fields = {
        'date': ['exact'],
        'workorder': ['exact'],
        'preventative_task': ['exact'],
    }
    field_order = [
        'date',
        'name',
        'request_type',
        'column_break',
        'preventative_task',
        'workorder',
        'requested_by',
        'section_break',
        'child:maintenance.sparesrequestitem'
    ]
    read_only_fields = ['date', 'name', 'requested_for', 'requested_by', 'request_type', 'status']

    date = models.DateField()
    name = models.CharField(max_length= 128, null=True)
    request_type = models.CharField(max_length= 128, null=True, choices=[
        ('request', 'Request'),
        ('issue', 'Issue'),
        ('return', 'Return'),
    ])
    status = models.CharField(max_length= 128, null=True, choices=[
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default="draft")
    requested_by = models.CharField(max_length= 128, null=True)
    preventative_task = models.ForeignKey('maintenance.preventativetask', on_delete=models.SET_NULL, null=True, blank=True)
    workorder = models.ForeignKey('maintenance.workorder', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "REQ-%06d" % self.pk

    def update_quantities(self):
        if self.status != "approved":
            return

        if self.request_type == "request":
            return

        const = -1 if self.request_type == "issue" else 1
        for row in self.sparesrequestitem_set.all():
            row.item.quantity += (row.quantity * const)
            row.item.save()

    def on_void(self):
        if self.status != "approved":
            return

        if self.request_type == "request":
            return

        const = 1 if self.request_type == "issue" else -1
        for row in self.sparesrequestitem_set.all():
            row.item.quantity += (row.quantity * const)
            row.item.save()

    def save(self, *args, **kwargs):
        self.update_quantities()
        super().save(*args, **kwargs)


class SparesRequestItem(models.Model):
    field_order = ['item', 'unit', 'quantity']
    update_read_only = True

    parent = models.ForeignKey('maintenance.sparesrequest', on_delete=models.CASCADE)
    item = models.ForeignKey("inventory.Item", null=True, on_delete=models.SET_NULL)
    unit = models.CharField(max_length = 32, null=True, blank=True)
    quantity = models.FloatField(default=0.0)