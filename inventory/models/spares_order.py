from __future__ import unicode_literals
from __future__ import division
from datetime import timedelta
import datetime
import os

from django.utils import timezone
from django.db import models
from django.db.models import Q

from base.models import BaseModel
from planning.models import RunPlanItem, Order

class SparesOrder(BaseModel):
    read_only_fields = ['status']
    dashboard_template = "inventory/approve_order.html"
    
    field_order = [
        'date',
        'order_number',
        'column_break',
        'supplier',
        'section_break',
        'child:inventory.sparesorderitem'
    ]

    date = models.DateField()
    order_number = models.CharField(max_length= 128)
    status = models.CharField(max_length= 128, null=True, choices=[
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default="draft")
    supplier = models.CharField(max_length= 128)

    def update_quantities(self):
        for row in self.sparesorderitem_set.all():
            row.item.quantity += row.quantity
            row.item.save()

    def save(self, *args, **kwargs):
        if self.status == "approved":
            self.update_quantities()
        super().save(*args, **kwargs)

    def __str__(self):
        return "ORDER-%06d" % self.pk

class SparesOrderItem(models.Model):
    field_order = ['item', 'unit', 'quantity']
    update_read_only = True

    parent = models.ForeignKey('inventory.sparesorder', on_delete=models.CASCADE)
    item = models.ForeignKey("inventory.Item", null=True, on_delete=models.SET_NULL)
    unit = models.CharField(max_length = 32, null=True, blank=True)
    quantity = models.FloatField(default=0.0)