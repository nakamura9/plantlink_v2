import os

from django.http import JsonResponse 

from inventory import forms
from django.views.generic import TemplateView, FormView
import threading
from inventory.utils import parse_file
from django.apps import apps
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.messages import info
from inventory.models import SparesOrder
from base.models import Account
from django.apps import apps 




class CSVImportDashboard(TemplateView):
    template_name = os.path.join("inventory", "dashboard.html")



class ImportView(FormView):
    form_class = forms.ImportForm
    template_name = os.path.join("inventory", "home.html")
    success_url = "/app/inventory/" 

    def form_valid(self, form):
        resp = super().form_valid(form)
        valid = False
        for ext in ["xlsx", "xls", "csv"]:
            if ext in form.cleaned_data['file'].name:
                valid = True
        if not valid:
            raise Exception("Invalid file extension")
        parse_file(form.cleaned_data['file'].file, form.cleaned_data['file'].name)
        # t = threading.Thread(target=parse_file, args=(form.cleaned_data['file'].file,))

        return resp


def get_all_children(request, model_name=None, id=None):
    model = apps.get_model(app_label='inventory', model_name=model_name)
    instance = model.objects.get(pk=id)
    children = instance.children
    if isinstance(children, dict):
        children = children.get('nodes')
    return JsonResponse({'data': children})

def update_spares_status(request, id=None):
    user= authenticate(username=request.GET['username'], password=request.GET['password'])
    if not user:
        info(request, "Wrong authentication")
        return HttpResponse("Error")
    status = request.GET['status']
    if not request.user.is_superuser:
        acc = Account.objects.get(pk= request.user.pk)
        if acc.role != "admin":
            info(request, "Only admins can approve or reject orders.")
            return HttpResponse("Error")
    
    
    app_label, model_name = request.GET['model'].split(".")
    model = apps.get_model(app_label=app_label, model_name=model_name)
    instance = model.objects.get(pk=id)
    instance.status = status
    instance.save()
    info(request, "Successfully updated status")
    return HttpResponse("Success")