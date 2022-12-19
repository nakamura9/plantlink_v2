
import os
import datetime

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import info
from django.contrib.auth import authenticate
from django.views.generic import TemplateView, FormView
from maintenance.models import WorkOrder, PreventativeTask, Checklist
from maintenance.models.checklists import ChecklistHistory, ChecklistItem
from django.http import HttpResponse
from base.models import Account
from django.apps import apps 
from maintenance.forms import ChecklistForm
from base.models import Account



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


class CheckListSubmitForm(FormView):
    form_class = ChecklistForm
    success_url = "/"
    template_name = os.path.join("maintenance", "checklist.html")

    def form_valid(self, form):
        checklist = Checklist.objects.get(pk=self.kwargs['id'])
        total_items = ChecklistItem.objects.filter(parent__id = self.kwargs['id'])
        all_items_set = set([i.pk for i in total_items])
        checked_items_set = set([int(i) for i in form.cleaned_data['checklist']])
        omitted_items = list(all_items_set.difference(checked_items_set))
        user = Account.objects.get(username=form.cleaned_data['username'])

        ChecklistHistory.objects.create(
            checklist=checklist,
            date=datetime.date.today(),
            resolver= user,
            no_items_completed = len(form.cleaned_data['checklist']),
            items_omitted = ",".join([str(i) for i in omitted_items])
        )
        info(self.request, f"Successfully completed checklist {checklist}")
        resp = super().form_valid(form)
        return resp
