from django.db import models
from base.models import BaseModel
from django.utils import timezone
import datetime


class RunPlanItem(BaseModel):
    class Meta:
        verbose_name = "Run Plan Item"
    list_fields = ['start_date', 'end_date', 'run_hours']
    dashboard_template = "planning/run_plan.html"

    filter_fields = {
        'machine': ['exact'],
        'start_date': ['exact']
    }
    field_order = [
        'machine',
        'start_date',
        'end_date',
        'column_break',
        'run_hours',
        'section_break',
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'column_break',
        'friday',
        'saturday',
        'sunday'
    ]

    start_date = models.DateField()
    end_date = models.DateField()
    run_hours = models.FloatField()
    
    machine = models.ForeignKey("inventory.Machine", null=True, on_delete=models.SET_NULL)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    #override save method to specify run days
    #add specific days
    #write property that gets total run hours  for a given period
    
    @property
    def orders(self):
        return Order.objects.filter(
            machine=self.machine, 
            manufacture_date__gte=self.start_date,
            manufacture_date__lte=self.end_date,
            )

    def __str__(self):
        return f'{self.start_date} to {self.end_date}'

    def is_running(self, day):
        if isinstance(day, datetime.datetime):
            day = day.date()
        #hasn't been applied yet
        if day < self.start_date or day > self.end_date:
            return False

        run_days = {0:self.monday,
                    1:self.tuesday,
                    2:self.wednesday,
                    3:self.thursday,
                    4:self.friday,
                    5:self.saturday,
                    6:self.sunday}
        
        return run_days[day.weekday()]

    @property
    def run_days(self):
        bools = [self.monday, self.tuesday, self.wednesday, self.thursday,
            self.friday, self.saturday, self.sunday]
        run_count = 0
        for b in bools:
            if b:
                run_count += 1
        return run_count

    @property
    def weekly_run_hours(self):
        return self.run_days * self.run_hours

    @property
    def total_run_hours(self):
        curr_day = self.start_date
        hours = 0
        while curr_day < self.end_date:
            if self.is_running(curr_day):
                hours += self.run_hours
            curr_day += datetime.timedelta(days=1)

        return hours



class Order(BaseModel):
    """
    Model representing customer order on which production calender is based.

    Fields: order_number, description, quantity, unit_price, manufacture_date, flute_profile(enum), liner(enum), layers(enum), delivery_date, customer, production_status(enum),delivery_status(enum)`
    
    """
    list_fields = ['customer', 'production_status', 'delivery_status']
    filter_fields = {
        'machine': ['exact'],
        'customer': ['icontains'],
        'production_status': ['exact'],
        'delivery_status': ['exact']
    }
    field_order = [
        'machine',
        'order_number',
        'description',
        'customer',
        'quantity',
        'column_break',
        'unit_price',
        'flute_profile',
        'liner',
        'layers', 
        'column_break',
        'manufacture_date',
        'delivery_date',
        'production_status',
        'delivery_status'
    ]

    def __init__(self, *args, **kwargs):
        self.actual_delivery_epoch = None
        super(Order,self).__init__(*args,**kwargs)

    machine = models.ForeignKey("inventory.Machine", null=True, on_delete=models.SET_NULL)
    order_number = models.CharField(max_length= 32, primary_key=True)
    description = models.CharField(max_length=64)
    quantity =models.IntegerField()
    unit_price = models.FloatField()
    manufacture_date = models.DateField()
    flute_profile = models.CharField(max_length=1, choices=[
        ("a", "A Flute"),
        ("b", "B Flute"),
        ("c", "C Flute"),
    ])
    liner = models.CharField(max_length=32, choices=[
        ("kraft", "Kraft"),
    ])
    layers = models.IntegerField(choices = [
        (1, "Single Wall Board"),
        (2, "Double Wall Board"),
    ]) 
    delivery_date = models.DateField()
    customer = models.CharField(max_length= 32)
    production_status = models.CharField(max_length=32, choices=[
        ("planned", "Planned"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed")
    ])
    delivery_status = models.CharField(max_length=16, choices = (
        ("storage", "In Storage"),
        ("transit", "In Transit"),
        ("delivered", "Delivered")
    ))

    def save(self, *args, **kwargs):
        if self.delivery_status == "delivered":
            self.actual_delivery_epoch = timezone.now().date()
        super(Order, self).save(*args, **kwargs)

    @property
    def actual_delivery_date(self):
        if self.delivery_status != "delivered":
            return "Undelivered"
        else:
            return self.actual_delivery_epoch.strftime("%d/%m/%Y")

    def __str__(self):
        return "%s: %s" % (self.order_number, self.description)