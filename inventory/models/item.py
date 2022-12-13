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


class Item(BaseModel):
    """
    Represents items retained in stock.
    """

    list_fields = ['serial_number', 'quantity', ]
    read_only_fields = ['quantity']
    filter_fields = {
        'name': ['icontains'],
        'serial_number': ['icontains'],
        'unit': ['exact']
    }
    field_order = [
        'name',
        'serial_number',
        'quantity',
        'unit',
        'column_break',
        'supplier',
        'unit_price',
        'min_stock_level',
        'reorder_quantity'
    ]

    serial_number = models.CharField(max_length= 32, primary_key=True)
    name = models.CharField(max_length= 32)
    quantity = models.IntegerField()
    unit = models.CharField(max_length= 32)
    supplier = models.CharField(max_length= 32)
    unit_price = models.FloatField()
    min_stock_level = models.IntegerField()
    reorder_quantity = models.IntegerField()

    def __str__(self):
        return self.name
