import os

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from maintenance.models import WorkOrder, PreventativeTask, Checklist


class Inbox(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = os.path.join("maintenance", "inbox.html")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breakdowns']  = WorkOrder.objects.filter(assigned_to__id=self.request.user.pk).exclude(status="approved")
        context['preventative_tasks'] = PreventativeTask.objects.filter(assignments__id__in=[self.request.user.pk], completed_date__isnull=True)
        context['checklists'] = Checklist.objects.filter(resolver__id=self.request.user.pk, on_hold=False)
        return context