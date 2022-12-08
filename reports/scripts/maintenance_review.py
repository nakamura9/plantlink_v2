from platform import machine
from inventory.models import Machine
from maintenance.models import WorkOrder, PreventativeTask, Checklist
from django.db.models import Q
import datetime
import pygal
from reports.utils import CustomStyle, calculate_spans, get_labels


def get_data(machine, dates, offset):
   if offset == 1:
      return [machine.availability_on_date(d) for d in dates]

   return [machine.availability_over_period(d, d + datetime.timedelta(days=offset)) for d in dates]




def render(filters):
   machines = "All Machines"
   frm = datetime.datetime.strptime(filters['from_date'], "%Y-%m-%d").date()
   to = datetime.datetime.strptime(filters['to_date'], "%Y-%m-%d").date()
   if filters.get('machine'):
      mech = Machine.objects.get(pk=filters['machine'])
      machines = str(mech)
      machine_filter = Q(machine=mech)
      
   else:
      
      machine_filter = Q(machine__pk__in=[i.pk for i in Machine.objects.all()])

   preventative = PreventativeTask.objects.filter(
         machine_filter,
         scheduled_for__gte=frm,
         scheduled_for__lte=to,
      )
   all_checklists = Checklist.objects.filter(
      machine_filter,
      on_hold=False
   )
   checklists = [
      check for check in all_checklists 
      if check.will_be_open_over_period(frm, to)
   ]
   breakdowns = WorkOrder.objects.filter(
      machine_filter,
      execution_date__gte=frm,
      execution_date__lte=to,
   )
   total_downtime = sum((t.downtime.seconds  \
            for  t in breakdowns if t.downtime)) / 3600.0

   dates, offsets = calculate_spans(frm, to)
   x_labels = get_labels(dates, offsets)
   

   machine_availability_chart = pygal.Bar(style=CustomStyle, x_label_rotation=15, height=400)
   machine_availability_chart.x_labels = x_labels
   if filters.get('machine'):
      data = get_data(mech, dates, offsets)
      machine_availability_chart.add("Availability", data)
   else:
      for mech in Machine.objects.all():
         data = get_data(mech, dates, offsets)
         machine_availability_chart.add(f"{mech} availability", data)

   overall_machine_availability_chart = pygal.Bar(style=CustomStyle, x_label_rotation=15, height=400)
   machine_availability_chart.x_labels = x_labels
   overall = []
   labels = []
   for mech in Machine.objects.all():
      overall.append(mech.availability_over_period(frm, to))
      labels.append(str(mech))
   overall_machine_availability_chart.x_labels = labels
   overall_machine_availability_chart.add(f"{mech} availability", overall)
   
   context = {
      'start_date': filters.get('from_date'),
      'end_date': filters.get('to_date'),
      'machines': machines,
      'p_tasks': preventative,
      'wos': breakdowns,
      'checks': checklists,
      'total_downtime': total_downtime,
      'machine_availability': machine_availability_chart.render(is_unicode=True),
      'overall_machine_availability': overall_machine_availability_chart.render(is_unicode=True)
   }
   return context

