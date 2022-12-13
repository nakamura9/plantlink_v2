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


class Machine(BaseModel):
    """
    Will be related to an asset and use its attributes.
    Level one equipment.
    Parent : Plant
    Child  : Section

    Example:
    ========
    Topra                                 <-Machine
        +--Feed Section
            +--Vacuum system
                +--Vacuum pump assembly
                    +--10 kW Motor

    Properties:
    ===========
    n_units -returns the number of units
    n_breakdowns(today/weekly/monthly/sixmonths) - returns number of breakdowns over the period
    checklist_coverage - how many units and sections are covered by a checklist versus the total number of units and sections

    Methods:
    ========
    availability_over_period
    planned_downtime_over_period
    unplanned_downtime_over_period
    run_hours_over_period
    ***
    """

    list_fields = ['manufacturer', 'commissioning_date']
    filter_fields = {
        'manufacturer': ['exact'],
        'machine_name': ['icontains']
    }
    field_order = [
        'machine_name',
        'asset_data',
        'unique_id',
        'column_break',
        'manufacturer',
        'commissioning_date',
        'section_break',
    ]

    dashboard_template = os.path.join("inventory", 'machine.html')

    machine_name = models.CharField(max_length=128)
    unique_id = models.CharField(max_length=24, primary_key=True)
    manufacturer = models.CharField(max_length=128)
    asset_data = models.ForeignKey("Asset", null=True, blank=True, verbose_name="Asset",on_delete=models.SET_NULL)
    commissioning_date = models.DateField(blank = True, null=True)
    

    def dashboard_context(self):
        return {
            "children_url": f'/get-all-children/machine/{self.pk}/'
        }

    @property
    def children(self):
        return [child.children for child in self.section_set.all()]

    @property
    def run_data(self):
        return RunPlanItem.objects.filter(machine=self)

    @property
    def orders(self):
        return Order.objects.filter(
            machine=self,
            manufacture_date__gte=datetime.date.today()
        )

    def availability_over_period(self, start, stop=datetime.date.today()):
        """used to calculate the machines availability over a given period"""
        downtime = self.unplanned_downtime_over_period(start, stop)
        available_time = self.run_hours_over_period(start, stop) - \
            self.planned_downtime_over_period(start, stop)

        if downtime > available_time:
            return 0
        elif available_time == 0:
            return 100 #?
        return ((available_time-downtime)/ available_time) * 100

    def planned_downtime_over_period(self, start, stop=datetime.date.today()):
        """used to calculate downtime over a period of time"""
        #come up with a variant for repeated tasks
        p_tasks = self.preventativetask_set.filter(Q(completed_date__gte=start) & Q(completed_date__lte=stop))
        if p_tasks.count() > 0:
            return sum((i.actual_downtime.seconds for i in p_tasks)) / 3600.0 

        return 0.0

    def unplanned_downtime_over_period(self, start, stop=datetime.date.today()):
        """used to calculate downtime over a period due to breakdowns"""
        wos = self.workorder_set.filter(Q(completion_date__gte=start) & Q(completion_date__lte=stop))
        if wos.count() > 0:
            return sum((i.downtime.seconds for i in wos)) / 3600.0
        return 0

    def run_hours_over_period(self, start, end):
        """calculate run data for a period of time.
        NB Very inefficient!
        """
        curr_day = start
        total_hours = 0
        while curr_day < end:
            for curr_run in self.run_on_date(curr_day):
                if curr_run.is_running(curr_day):
                    total_hours += curr_run.run_hours
            curr_day += datetime.timedelta(days=1)        
        return total_hours

    def availability_on_date(self, date):
        """Returns the machine availability for that date"""
        breakdowns = self.workorder_set.filter(execution_date=date)
        if breakdowns.count() > 0:
            downtime = sum(i.downtime.seconds for i in breakdowns if i.downtime) /3600.0
        else: 
            downtime = 0.0
        run_data = self.run_on_date(date)
        
        if run_data:
            available_time = sum((run.run_hours for run in run_data \
                if run.is_running(date)))
            if downtime > available_time:
                return 0.0
            return ((available_time - downtime)/ available_time) * 100
        
        else:
            return 100.0

    def run_on_date(self, date):
        """returns the run data for the stated date
        """
        return self.run_data.filter(
            Q(start_date__lte=date) & Q(end_date__gte=date))

    def is_running_on_date(self, date):
        """used on the planning application"""
        run_set = self.run_on_date(date)
        for run in run_set:
            if run.is_running(date):
                return True
        return False

    def __str__(self):
        return self.machine_name

    @property
    def recent_run_data(self):
        return self.run_data.all().order_by("start_date")[:5]

    @property
    def n_breakdowns_today(self):
        yesterday = timezone.now() - timedelta(days=1)
        return self.workorder_set.filter(execution_date__gt = yesterday).count()

    @property
    def n_breakdowns_weekly(self):
        week = timezone.now() - timedelta(days=7)
        return self.workorder_set.filter(execution_date__gt = week).count()


    @property
    def n_breakdowns_monthly(self):
        month = timezone.now() - timedelta(days=30)
        return self.workorder_set.filter(execution_date__gt = month).count()

    @property
    def n_breakdowns_sixmonths(self):
        bi_ann = timezone.now() - timedelta(days=182)
        return self.workorder_set.filter(execution_date__gt = bi_ann).count()
