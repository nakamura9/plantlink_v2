import os

from django.http import JsonResponse 

from inventory import forms
from django.views.generic import TemplateView, FormView
import threading
from inventory.utils import parse_file
from django.apps import apps



class CSVImportDashboard(TemplateView):
    template_name = os.path.join("inventory", "dashboard.html")



class ImportView(FormView):
    form_class = forms.ImportForm
    template_name = os.path.join("inventory", "home.html")
    success_url = "/csv-dashboard/" 

    def form_valid(self, form):
        resp = super().form_valid(form)
        parse_file(form.cleaned_data['file'].file)
        # t = threading.Thread(target=parse_file, args=(form.cleaned_data['file'].file,))

        return resp


def get_all_children(request, model_name=None, id=None):
    model = apps.get_model(app_label='inventory', model_name=model_name)
    instance = model.objects.get(pk=id)
    children = instance.children
    if isinstance(children, dict):
        children = children.get('nodes')
    return JsonResponse({'data': children})