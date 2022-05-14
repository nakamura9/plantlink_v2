from reports.utils import get_breakdowns, get_downtime
import datetime 
from inventory.models import Machine 
from django.db.models import Q

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

   breakdowns = get_breakdowns(machine_filter, frm, to)
   total_downtime = get_downtime(breakdowns)


   context = {
      'wos': breakdowns,
      'total_downtime': total_downtime,
      'machines': machines,
      'start_date': filters.get('from_date'),
      'end_date': filters.get('to_date'),
   }
   return context

