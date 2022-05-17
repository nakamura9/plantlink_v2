from pygal.style import BlueStyle
import datetime
from inventory.models import Machine 
from django.db.models import Q
from maintenance.models import WorkOrder

CustomStyle = BlueStyle(
    label_font_size=16,
    major_label_font_size=20,
    legend_font_size=16,
    font_family='sans-serif',
    title_font_size=20,
    guide_stroke_dasharray='0',
    major_guide_stroke_dasharray='0',
    value_colors=('white', ),
    background="transparent",
    colors=('#23374d', '#007bff', '#4682b4', '#1089ff',
            '#00bfff', '#191970', '#B0C4DE', '#B0E0E6',)
)

def calculate_spans(frm, to):
   span = (to - frm).days
   
   if span < 14:
      date_range = 1
   elif span < 60:
      date_range = 7
   else:
      date_range = 28

   dates = []
   curr_date = frm
   offset = 0
   while curr_date < to:
      curr_date = frm + datetime.timedelta(days=offset)
      dates.append(curr_date)
      offset += date_range

   return dates, date_range

def get_labels(dates, offsets):
   if offsets == 1:
      return [str(d) for d in dates]

   if offsets == 7:
      return [f"Week {i} ({str(d)})" for i, d in enumerate(dates, start=1)]

   return [f"Month {i} ({d.strftime('%B %Y')})" for i, d in enumerate(dates, start=1)]


def get_breakdowns(mech, frm, to):
   if isinstance(mech, Machine):
      f = Q(machine=mech)
   else: # Q object
      f = mech
   return WorkOrder.objects.filter(
      f,
      execution_date__gte=frm,
      execution_date__lte=to,
   )

def get_downtime(breakdowns):
   return sum(t.downtime.seconds  \
            for  t in breakdowns if t.downtime) / 3600.0