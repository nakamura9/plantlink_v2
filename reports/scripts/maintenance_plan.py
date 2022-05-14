from turtle import heading
import pygal 
from reports.utils import CustomStyle, calculate_spans, get_labels
import datetime
from django.db.models import Q
from inventory.models import Machine
from maintenance.models import WorkOrder, PreventativeTask, Checklist


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
   scheduled_downtime = sum(i.estimated_downtime.seconds for i in preventative if i.estimated_downtime ) / 3600.0

   context = {
      'start_date': filters.get('from_date'),
      'end_date': filters.get('to_date'),
      'p_task_count': preventative.count(),
      'check_count': all_checklists.count(),
      'scheduled_downtime': scheduled_downtime,
      'machines': machines,
      'p_tasks': preventative,
      'checks': all_checklists
   }
   return context

