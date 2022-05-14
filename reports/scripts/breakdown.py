from turtle import heading
import pygal 
from reports.utils import (
   CustomStyle, calculate_spans, get_labels, get_breakdowns,
   get_downtime
)
import datetime
from django.db.models import Q
from inventory.models import Machine
from maintenance.models import WorkOrder, PreventativeTask




def get_planned(mech, frm, to):
   if isinstance(mech, Machine):
      f = Q(machine=mech)
   else: # Q object
      f = mech
   return PreventativeTask.objects.filter(
      f,
      scheduled_for__gte=frm,
      scheduled_for__lte=to,
   )



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
   
   all_machines = Machine.objects.all()
   combined_breakdown_frequency = pygal.Bar(style=CustomStyle, height=400)
   combined_breakdown_frequency.x_labels = [str(mech) for mech in all_machines]
   combined_breakdown_frequency.add(
      "Breakdown Count",
      [get_breakdowns(mech, frm, to).count() for mech in all_machines]
   )

   combined_breakdown_hours = pygal.Bar(style=CustomStyle, height=400)
   combined_breakdown_hours.x_labels = [str(mech) for mech in all_machines]
   combined_breakdown_hours.add(
      "Breakdown Hours",
      [get_downtime(get_breakdowns(mech, frm, to)) for mech in all_machines]
   )

   dates, offset = calculate_spans(frm, to)

   breakdowns_by_time = pygal.Bar(style=CustomStyle, height=400, x_label_rotation=15)
   breakdowns_by_time.x_labels = get_labels(dates, offset)
   breakdowns_by_time.add(f"{machines} hours", [
      get_downtime(get_breakdowns(machine_filter, d, d + datetime.timedelta(days=offset))) for d in dates
   ])
   breakdowns_by_time.add(f"{machines} count", [
      get_breakdowns(machine_filter, d, d + datetime.timedelta(days=offset)).count() for d in dates
   ])

   planned_vs_unplanned = pygal.Bar(style=CustomStyle, height=400, x_label_rotation=15)
   planned_vs_unplanned.x_labels = get_labels(dates, offset)
   planned_vs_unplanned.add("Planned Jobs", [
      get_planned(machine_filter, d, d + datetime.timedelta(days=offset)).count() for d in dates
   ])

   planned_vs_unplanned.add("Breakdowns", [
      get_breakdowns(machine_filter, d, d + datetime.timedelta(days=offset)).count() for d in dates
   ])

   context = {
      'wos': breakdowns,
      'total_downtime': total_downtime,
      'start_date': filters.get('from_date'),
      'end_date': filters.get('to_date'),
      'machines': machines,
      "combined_breakdown_frequency": combined_breakdown_frequency.render(is_unicode=True),
      "combined_breakdown_hours": combined_breakdown_hours.render(is_unicode=True),
      "breakdowns_by_time": breakdowns_by_time.render(is_unicode=True),
      "planned_vs_unplanned": planned_vs_unplanned.render(is_unicode=True)
   }
   return context

