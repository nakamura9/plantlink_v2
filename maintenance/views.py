
import os

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import info
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from maintenance.models import WorkOrder, PreventativeTask, Checklist
from django.http import HttpResponse
from base.models import Account
from django.apps import apps 



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
    if not request.user.is_superuser:
        acc = Account.objects.get(pk= request.user.pk)
        if status in ['approved', 'declined'] and acc.role != "admin":
            info(request, "Only admins can approve or reject jobs.")
            return HttpResponse("Goodbye world")

    app_label, model_name = request.GET['model'].split(".")
    model = apps.get_model(app_label=app_label, model_name=model_name)

    instance = model.objects.get(pk=id)
    instance.status = status
    instance.save()
    info(request, "Successfully updated status")
    return HttpResponse("Success")
