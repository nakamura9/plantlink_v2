from __future__ import unicode_literals
import datetime

from django.db import models
from django.utils import timezone

from base.utilities import time_choices
from base.models import BaseModel


def now():
    return datetime.datetime.now().strftime("%H%M")

class Checklist(BaseModel):
    """
    Data representation of a checklist
    Properties
    ==========
    is_open -> Boolean
    get_type -> string
    next -> timedelta
    
    Methods
    ==========
    will_be_open_over_period(start, stop) 2 date objects return bool
    is_open_on_date(date) date object returns bool
    """

    list_fields = ['machine', 'section', 'resolver']
    read_only_fields = [
        'title', 'creation_date', 'last_completed_date',
        'estimated_time', 'start_time', 'resolver', 'category', 'frequency',
        'machine', 'section', 'subunit', 'subassembly', 'component'
    ]
    filter_fields = {
        'machine': ['exact'],
        'resolver': ['exact'],
        'category': ['exact'],
    }
    field_order = [
        'title',
        'creation_date',
        'last_completed_date',
        'estimated_time',
        'start_time',
        'resolver',
        'category',
        'frequency',
        'on_hold',
        "child:maintenance.checklistcomment",
        'column_break',
        'machine',
        'section',
        'subunit',
        'subassembly',
        'component',
        "child:maintenance.checklistitem",
        
    ]
    
    mapping =  {"daily": 1,
        "weekly": 7,
        "fortnightly": 14,
        "monthly": 30,
        "quarterly": 90,
        "bi-annually": 180,
        "yearly": 360}


    title = models.CharField(max_length= 64)
    creation_date = models.DateField()
    last_completed_date = models.DateField(blank = True, null=True)
    estimated_time= models.DurationField(choices = [] \
                        + time_choices("00:05:00", "00:35:00", 
                                        "00:05:00", delta=True) \
                         + time_choices("01:00:00", "08:01:00", 
                                        "01:00:00", delta=True))
    start_time = models.TimeField(choices=time_choices(
                                            "06:30:00", "17:30:00", "00:30:00"))
    machine = models.ForeignKey("inventory.Machine", on_delete=models.CASCADE)
    section = models.ForeignKey("inventory.Section", 
                null=True, blank=True, on_delete=models.SET_NULL)
    subunit = models.ForeignKey("inventory.SubUnit", 
                null=True, blank=True, on_delete=models.SET_NULL)
    subassembly = models.ForeignKey("inventory.SubAssembly", 
                null=True, blank=True, on_delete=models.SET_NULL)
    component = models.ForeignKey("inventory.Component", 
                null=True, blank=True, on_delete=models.SET_NULL)
    resolver = models.ForeignKey("base.Account", on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length = 64,
                    choices=[("electrical", "Electrical"),
                    ("mechanical", "Mechanical")])
    frequency = models.CharField(max_length = 16, 
                        choices = [("daily", "Daily"),
                                    ("weekly", "Weekly"),
                                    ("fortnightly", "Every 2 weeks"),
                                    ("monthly", "Monthly"),
                                    ("quarterly", "Every 3 Months"),
                                    ("bi-annually", "Every 6 Months"), 
                                    ("yearly", "Yearly")])
    on_hold = models.BooleanField(default=False)
    
    def will_be_open_over_period(self, start, stop):
        """method used in reports to filter checklists that will not be undertaken during the stated period"""
        curr = start
        if self.on_hold:
            return False

        #quick determination if possible
        if self.next is not None:
            if self.next >= start and self.next < stop:
                return True 

        #manual technique
        while curr < stop:
            if self.is_open_on_date(curr):
                return True
            else:
                curr = curr +datetime.timedelta(days=1)
            
        return False

    def is_open_on_date(self, date):
        if self.on_hold:
            return False
        
        if self.last_completed_date is None:
            return True
        else:
            delta = date - self.last_completed_date

        if delta.days > self.mapping[self.frequency]:
            return True
        else:
            return False
    
    def __str__(self):
        return self.title
    
    @property
    def is_open(self):
        return self.is_open_on_date(datetime.date.today())
    
    @property
    def next(self):
        "determine the next date for a checklist"
        if self.last_completed_date:
            return self.last_completed_date + \
            datetime.timedelta(days=self.mapping[self.frequency])

    @property
    def get_type(self):
        return "checklist"

    def save(self, *args, **kwargs):
        if self.pk:
            self.last_completed_date = datetime.date.today()

        super().save(*args, **kwargs)


class ChecklistItem(models.Model):
    field_order = ['description']
    update_read_only = True

    class Meta:
        verbose_name = "Checklist Item"

    parent = models.ForeignKey('maintenance.checklist', on_delete=models.CASCADE)
    description = models.TextField()


class ChecklistComment(models.Model):
    field_order = ['content']
    update_add_only = True

    class Meta:
        verbose_name = "Comment"

    parent = models.ForeignKey('maintenance.checklist', on_delete=models.CASCADE)
    content = models.TextField()
    # author = models.ForeignKey('auth.user', on_delete=models.CASCADE)
