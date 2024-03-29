from django.shortcuts import render
from django.views.generic import TemplateView
import os
from reports.models import Report
from django.http.response import HttpResponse, JsonResponse
from django.forms import ValidationError
from django.template import loader
from wkhtmltopdf.views import PDFTemplateView
from django.contrib.messages import info
from base.models import BaseModel, Account
from django.http import  HttpResponseRedirect

class HomeView(TemplateView):
    template_name = os.path.join('reports', 'home.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.all()
        return context


class ReportView(TemplateView):
    template_name = os.path.join("reports", "report.html")

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        if self.request.user.is_superuser:
            return resp
        acc = Account.objects.get(pk=self.request.user.pk)
        if acc.role in ["admin", "maintenance_planner", "production_planner", "inventory_controller"]:
            return resp 
        
        info(self.request, f"{self.request.user} does not have sufficient permissions to access this page")
        return HttpResponseRedirect('/home/')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = Report.objects.get(name=self.kwargs['name'])
        context['form'] = report.get_form_class()

        return context

def get_report_data(request, name=None):
    report = Report.objects.get(name=name)
    template = loader.get_template(report.template_path)
    try:
        context = report.render_func(request.POST)
    except ValidationError as e:
        return JsonResponse({"error": str(e)})
    except Exception as ex:
        raise ex


    content = template.render(context, request)
    return HttpResponse(content)


class ReportPDFView(PDFTemplateView):
    def get_template_names(self):
        report = Report.objects.get(name=self.kwargs['name'])
        return [ report.template_path ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = Report.objects.get(name=self.kwargs['name'])
        data = report.render_func(self.request.GET)
        context.update(data)
        return context
