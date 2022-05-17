from reports.utils import (
   CustomStyle, calculate_spans, get_labels,
   get_breakdowns, get_downtime)
import datetime 
from inventory.models import Machine 
from django.db.models import Q
import pygal 


def safe_max(iterable, key=None):
   if not iterable:
      return ('', 0)

   return max(iterable, key=key)


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
   machine_breakdown_frequency = {}
   machine_breakdown_duration = {}
   section_breakdown_frequency = {}
   section_breakdown_duration = {}
   component_breakdown_frequency = {}
   component_breakdown_duration = {}

   for breakdown in breakdowns:
      machine = str(breakdown.machine)
      
      machine_breakdown_duration.setdefault(machine, 0)
      machine_breakdown_frequency.setdefault(machine, 0)
      machine_breakdown_frequency[machine] += 1
      machine_breakdown_duration[machine] += breakdown.downtime_hours
      if breakdown.section:
         section = str(breakdown.section)
         section_breakdown_duration.setdefault(section, 0)
         section_breakdown_frequency.setdefault(section, 0)
         section_breakdown_frequency[section] += 1
         section_breakdown_duration[section] += breakdown.downtime_hours

      if breakdown.component:
         component = str(breakdown.component)
         component_breakdown_duration.setdefault(component, 0)
         component_breakdown_frequency.setdefault(component, 0)
         component_breakdown_frequency[component] += 1         
         component_breakdown_duration[component] += breakdown.downtime_hours

   total_downtime = get_downtime(breakdowns)
   max_machine_frequency = safe_max(machine_breakdown_frequency.items(), key=lambda x: x[1])
   max_machine_duration = safe_max(machine_breakdown_duration.items(), key=lambda x: x[1])
   max_section_frequency = safe_max(section_breakdown_frequency.items(), key=lambda x: x[1])
   max_section_duration = safe_max(section_breakdown_duration.items(), key=lambda x: x[1])
   max_component_frequency = safe_max(component_breakdown_frequency.items(), key=lambda x: x[1])
   max_component_duration = safe_max(component_breakdown_duration.items(), key=lambda x: x[1])
   

   machine_frequency_against_hours = pygal.Bar(style=CustomStyle, height=400, x_label_rotation=15)
   x_labels = list(machine_breakdown_frequency.keys())
   machine_frequency_against_hours.x_labels = x_labels
   machine_frequency_against_hours.add("Frequency", [machine_breakdown_frequency.get(x, 0) for x in x_labels])
   machine_frequency_against_hours.add("Duration", [machine_breakdown_duration.get(x, 0) for x in x_labels])

   section_frequency_against_hours = pygal.Bar(style=CustomStyle, height=400, x_label_rotation=15)
   x_labels = list(section_breakdown_frequency.keys())
   section_frequency_against_hours.x_labels = x_labels
   section_frequency_against_hours.add("Frequency", [section_breakdown_frequency.get(x, 0) for x in x_labels])
   section_frequency_against_hours.add("Duration", [section_breakdown_duration.get(x, 0) for x in x_labels])

   component_frequency_against_hours = pygal.Bar(style=CustomStyle, height=400, x_label_rotation=15)
   x_labels = list(component_breakdown_frequency.keys())
   component_frequency_against_hours.x_labels = x_labels
   component_frequency_against_hours.add("Frequency", [component_breakdown_frequency.get(x, 0) for x in x_labels])
   component_frequency_against_hours.add("Duration", [component_breakdown_duration.get(x, 0) for x in x_labels])

   context = {
      'wos': breakdowns,
      'total_downtime': total_downtime,
      'machines': machines,
      'start_date': filters.get('from_date'),
      'end_date': filters.get('to_date'),
      'max_machine_downtime': max_machine_duration[1],
      'max_machine_frequency': max_machine_frequency[1],
      'max_downtime_machine': max_machine_duration[0],
      'max_frequency_machine': max_machine_frequency[0],
      'max_section_downtime': max_section_duration[1],
      'max_section_frequency': max_section_frequency[1],
      'max_downtime_section': max_section_duration[0],
      'max_frequency_section': max_section_frequency[0],
      'max_component_downtime': max_component_duration[1],
      'max_component_frequency': max_component_frequency[1],
      'max_downtime_component': max_component_duration[0],
      'max_frequency_component': max_component_frequency[0],
      'machine_frequency_vs_duration': machine_frequency_against_hours.render(is_unicode=True),
      'section_frequency_vs_duration': section_frequency_against_hours.render(is_unicode=True),
      'component_frequency_vs_duration': component_frequency_against_hours.render(is_unicode=True)
   }
   return context
