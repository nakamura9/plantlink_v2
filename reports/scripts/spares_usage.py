from inventory.models import Machine
from django.db.models import Q
import datetime
from maintenance.models import PreventativeTask
from reports.utils import get_breakdowns

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

   breakdowns = get_breakdowns(machine_filter, frm, to)

   spares_count = sum(task.required_spares.all().count() for task in preventative)
   spares_count += sum(wos.spares_issued.all().count() - wos.spares_returned.all().count() for wos in breakdowns)

   context = {
      'start_date': filters.get('from_date'),
      'end_date': filters.get('to_date'),
      'machines': machines,
      'p_tasks': preventative,
      'spares_count': spares_count,
      'wos': breakdowns

   }
   return context

