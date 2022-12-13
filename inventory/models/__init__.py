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

from .spares_order import SparesOrder, SparesOrderItem

from .machine import Machine
from .item import Item


class Asset(BaseModel):
    """
    Model that represents a company asset.

    #Should act as the Machine model base class

    """
    list_fields = []
    filter_fields = {}
    field_order = [
        'asset_unique_id',
        'column_break'
    ]
    asset_unique_id = models.CharField(max_length=32, unique=True)
    

    def __str__(self):
        return self.asset_unique_id


class Plant(BaseModel):
    """
    Used to distinguish main plant from sheet plant
    Might be deprecated soon. 
    """

    
    filter_fields = {
        'plant_name': ['icontains']
    }
    field_order = [
        'plant_name'
    ]
    plant_name= models.CharField(max_length = 128)
    
    def __str__(self):
        return self.plant_name


class Section(BaseModel):
    """
    Level 2
    parent: Machine
    child : Subunit
    
    Example:
    =======
    Topra                                 
        +--Feed Section                 <-Section
            +--Vacuum system
                +--Vacuum pump assembly
                    +--10 kW Motor
    """
    list_fields = ['machine']
    filter_fields = {
        'machine': ['exact']
    }
    field_order = [
        'section_name',
        'machine',
        'unique_id'
    ]

    unique_id = models.CharField(max_length=24, primary_key=True)
    section_name = models.CharField(max_length=64)
    machine= models.ForeignKey("Machine", null=True, on_delete=models.SET_NULL)

    dashboard_template = os.path.join("inventory", 'section.html')

    def dashboard_context(self):
        return {"children_url": f'/get-all-children/section/{self.pk}/'}

    @property
    def children(self):
        return {
            'label': str(self),
            'id': self.pk,
            'nodes': [child.children for child in self.subunit_set.all()]
        }

    def __str__(self):
        return self. section_name


class SubUnit(BaseModel):
    """
    Level 3
    parent : Section
    child  : SubAssembly

    Example:
    =======
    Topra                                 
        +--Feed Section                 
            +--Vacuum system            <-SubUnit
                +--Vacuum pump assembly
                    +--10 kW Motor
    """

    list_fields = ['machine', 'section']
    filter_fields = {
        'machine': ['exact'],
        'section': ['exact']
    }
    field_order = [
        'unit_name',
        'machine',
        'section',
        'unique_id'
    ]
    
    unique_id = models.CharField(max_length=24, primary_key=True)
    unit_name = models.CharField(max_length=128)
    machine = models.ForeignKey("Machine", null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey("Section", null=True, on_delete=models.SET_NULL)
    
    dashboard_template = os.path.join("inventory", 'section.html')

    def dashboard_context(self):
        return {"children_url": f'/get-all-children/subunit/{self.pk}/'}

    def __str__(self):
        return self.unit_name

    @property
    def children(self):
        return {
            'label': str(self),
            'id': self.pk,
            'nodes': [child.children for child in self.subassembly_set.all()]
        }


class SubAssembly(BaseModel):
    """
    Level 4
    parent : Subunit
    child  : Component

    Example:
    =======
    Topra                                 
        +--Feed Section                 
            +--Vacuum system            
                +--Vacuum pump assembly <-Sub Assembly
                    +--10 kW Motor
    """

    list_fields = ['machine', 'section', 'subunit']
    filter_fields = {
        'machine': ['exact'],
        'section': ['exact'],
        'subunit': ['exact']
    }
    field_order = [
        'unit_name',
        'unique_id',
        'column_break',
        'machine',
        'section',
        'subunit'
    ]
    unique_id = models.CharField(max_length=24, primary_key=True)
    unit_name = models.CharField(max_length=128, verbose_name="Name")
    subunit = models.ForeignKey("SubUnit", null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey("Section", null=True, on_delete=models.SET_NULL)
    machine = models.ForeignKey("Machine", null=True, on_delete=models.SET_NULL)
    
    dashboard_template = os.path.join("inventory", 'section.html')

    def dashboard_context(self):
        return {"children_url": f'/get-all-children/subassembly/{self.pk}/'}

    def __str__(self):
        return self.unit_name

    @property
    def children(self):
        return {
            'label': str(self),
            'id': self.pk,
            'nodes': [{"label": str(child), 'id': self.pk, 'nodes': []} for child in self.component_set.all()]
        }


class Component(BaseModel):
    """
    Level 5
    parent : SubAssembly
    child  : None
    

    Example:
    =======
    Topra                                 
        +--Feed Section                 
            +--Vacuum system
                +--Vacuum pump assembly
                    +--10 kW Motor      <-Component
    """

    list_fields = ['machine', 'section', 'subunit', 'subassembly']
    filter_fields = {
        'component_name': ['icontains'],
        'machine': ['exact'],
        'section': ['exact'],
        'subunit': ['exact'],
        'subassembly': ['exact'],
    }
    field_order = [
        'component_name',
        'unique_id',
        'spares_data',
        'column_break',
        'machine',
        'section',
        'subunit',
        'subassembly'
    ]
    unique_id = models.CharField(max_length=24, primary_key=True)
    component_name = models.CharField(max_length = 128)
    machine = models.ForeignKey("Machine", null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey("Section", null=True, on_delete=models.SET_NULL)
    subunit = models.ForeignKey("SubUnit", null=True, blank=True,
        on_delete=models.SET_NULL)
    subassembly = models.ForeignKey("SubAssembly", null=True, on_delete=models.SET_NULL)
    spares_data=models.ManyToManyField("Item",verbose_name="linked spares")

    dashboard_template = os.path.join("inventory", 'component.html')
    
    def __str__(self):
        return self.component_name
