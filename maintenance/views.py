
import os

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import info
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from maintenance.models import WorkOrder, PreventativeTask, Checklist
from django.http import HttpResponse

class Inbox(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = os.path.join("maintenance", "inbox.html")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breakdowns']  = WorkOrder.objects.filter(assigned_to__id=self.request.user.pk).exclude(status="approved")
        context['preventative_tasks'] = PreventativeTask.objects.filter(assignments__id__in=[self.request.user.pk], completed_date__isnull=True)
        context['checklists'] = Checklist.objects.filter(resolver__id=self.request.user.pk, on_hold=False)
        return context


def update_status(request, id=None):
    user= authenticate(username=request.GET['username'], password=request.GET['password'])
    if not user:
        info(request, "Wrong authentication")
        return HttpResponse("Goodbye world")
    status = request.GET['status']
    if status in ['approved', 'declined'] and request.user.role != "admin":
        info(request, "Only admins can approve or reject jobs.")
        return HttpResponse("Goodbye world")

    job = WorkOrder.objects.get(pk=id)
    job.status = status
    job.save()
    info(request, "Successfully updated status")
    return HttpResponse("Goodbye world")