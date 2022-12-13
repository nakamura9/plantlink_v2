from datetime import datetime
import os 

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from maintenance.models import Checklist, PreventativeTask
from inventory.models import Machine
import calendar
import datetime
import json

class CalendarView(TemplateView):
    template_name = os.path.join("planning", "calendar.html")


def month(request, year=None, month=None):
    ''' Javascript uses 0 indexed dates '''
    month = month + 1
    _, length = calendar.monthrange(year, month)
    start = datetime.date(year, month, 1)
    end = datetime.date(year, month, length)
    days = [datetime.date(year, month, i) for i in range(1, length + 1)]

    try:
        args = json.loads(request.body)
    except:
        args = {}

    filters = args.get('filters', {})


    checklists = Checklist.objects.filter(
        resolver__id=request.user.pk,
        on_hold=False
    )
    machines = Machine.objects.all()
    planned_jobs = PreventativeTask.objects.filter(
        # assignments__id__in=[request.user.pk],
        completed_date__isnull=True,
        scheduled_for__gte=start,
        scheduled_for__lte=end
    )

    events = []
    if filters.get('event_types') in ['production', None]:
        for mech in machines:
            span = 0
            first_day = None
            for day in days:
                if mech.is_running_on_date(day):
                    span += 1
                    if span == 1:
                        first_day = day
                else:
                    if span > 0:
                        events.append({
                            'date': first_day,
                            'title': f"RUN: {mech}",
                            'description': "Machine Running",
                            'span': span,
                            'id': f"/update/inventory/machine/{mech.unique_id}",
                            'next': None
                        })
                        span = 0 
    if filters.get('event_types') in ['maintenance', None]: 
        for day in days:
            for checklist in checklists:
                if checklist.is_open_on_date(day):
                    events.append({
                        'date': day,
                        'title': f"C: {checklist.title}",
                        'description': str(checklist.machine),
                        'span': 1,
                        'id': f"/update/maintenance/checklist/{checklist.pk}",
                        'next': None
                    })

        for job in planned_jobs:
            events.append({
                'date': job.scheduled_for,
                'title': f"PT: {job.machine}",
                'description': job.description,
                'span': 1,
                'id': f"/update/maintenance/preventativetask/{job.pk}",
                'next': None
            })

    return JsonResponse(events, safe=False)


def week(request, year=None, month=None, day=None):
    ''' Javascript uses 0 indexed dates '''
    try:
        args = json.loads(request.body)
    except:
        args = {}

    filters = args.get('filters', {})

    month = month + 1
    current_date = datetime.date(year, month, day)
    curr_weekday = current_date.isoweekday()
    start = current_date + datetime.timedelta(days=(0 - curr_weekday))
    end = current_date + datetime.timedelta(days=(7 - curr_weekday))
    machines = Machine.objects.all()
    
    days = [datetime.date(year, month, i) for i in range(start.day, end.day)]
    
    checklists = Checklist.objects.filter(
        resolver__id=request.user.pk,
        on_hold=False
    )
    planned_jobs = PreventativeTask.objects.filter(
        # assignments__id__in=[request.user.pk],
        completed_date__isnull=True,
        scheduled_for__gte=start,
        scheduled_for__lte=end
    )
    events = []
    for day in days:
        if filters.get('event_types') in ['maintenance', None]:
            for checklist in checklists:
                if checklist.is_open_on_date(day):
                    events.append({
                        'date': day,
                        'title': f"C: {checklist.title}",
                        'description': str(checklist.machine),
                        'span': 1,
                        'id': f"/update/maintenance/checklist/{checklist.pk}",
                        'next': None
                    })
        if filters.get('event_types') in ['production', None]:
            for mech in machines:
                if mech.is_running_on_date(day):
                    events.append({
                        'date': day,
                        'title': f"RUN: {mech}",
                        'description': "Machine Running",
                        'span': 1,
                        'id': f"/update/inventory/machine/{mech.unique_id}",
                        'next': None
                    })

    if filters.get('event_types') in ['maintenance', None]:
        for job in planned_jobs:
            events.append({
                'date': job.scheduled_for,
                'title': f"PT: {str(job.machine)}",
                'description': job.description,
                'span': 1,
                'id': f"/update/maintenance/preventativetask/{job.pk}",
                'next': None
            })
    return JsonResponse(events, safe=False)


def day(request, year=None, month=None, day=None):
    ''' Javascript uses 0 indexed dates '''
    try:
        args = json.loads(request.body)
    except:
        args = {}

    filters = args.get('filters', {})

    month = month + 1
    current_date = datetime.date(year, month, day)
    checklists = Checklist.objects.filter(
        resolver__id=request.user.pk,
        on_hold=False
    )
    machines = Machine.objects.all()

    planned_jobs = PreventativeTask.objects.filter(
        assignments__id__in=[request.user.pk],
        completed_date__isnull=True,
        scheduled_for=current_date
    )

    events = []
    if filters.get('event_types') in ['maintenance', None]:
        for checklist in checklists:
            if checklist.is_open_on_date(current_date):
                events.append({
                    'date': current_date,
                    'title': f"C: {checklist.title}",
                    'description': str(checklist.machine),
                    'span': 1,
                    'id': f"/update/maintenance/checklist/{checklist.pk}",
                    'next': None
                })

        for job in planned_jobs:
            events.append({
                'date': job.scheduled_for,
                'title': f"PT: {str(job.machine)}",
                'description': job.description,
                'span': 1,
                'id': f"/update/maintenance/preventativetask/{job.pk}",
                'next': None
            })
    if filters.get('event_types') in ['production', None]:
        for mech in machines:
            if mech.is_running_on_date(current_date):
                events.append({
                    'date': day,
                    'title': f"RUN: {mech}",
                    'description': "Machine Running",
                    'span': 1,
                    'id': f"/update/inventory/machine/{mech.unique_id}",
                    'next': None
                })
    return JsonResponse(events, safe=False)