import os

from django.http import  HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import  reverse
from django.views.generic import (
    FormView, ListView, CreateView,
    UpdateView, DeleteView, TemplateView
)
from django.apps import apps
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.authtoken.models import Token
from django.middleware.csrf import get_token

from base import forms
from base.models import BaseModel
from base.model_utils import child_table_fields
import json
import urllib
from django.db.models import Q
from django.db import models


class LoginView(FormView):
    template_name = os.path.join("base", "login.html")
    success_url = "/home"
    form_class = forms.LoginForm

    def form_valid(self, form):
        user= authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        auth_login(self.request, user)
        return super().form_valid(form)


def logout(request):
    from django.contrib.auth import logout as auth_logout
    if request.user.is_authenticated:
        auth_logout(request)

    return HttpResponseRedirect(reverse("login"))


class ModelMixin(object):
    def get_model_class(self):
        app = self.kwargs['app']
        model_name = self.kwargs['model']
        self._model = apps.get_model(app_label=app, model_name=model_name)
        return self._model


class HomeView(TemplateView):
    template_name = os.path.join("base", "home.html")


class AppHome(TemplateView):
    template_name = os.path.join("base", "app_home.html")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app = self.kwargs['app']
        context['app_name'] = app.title()
        context['app'] = app
        models = apps.all_models[app]
        links = []
        for model in models.values():
            if not hasattr(model, "home_visible"):
                continue
            links.append({
                'url': f'/list/{app}/{model._meta.model_name}/',
                'name': model._meta.verbose_name.title()
            })

        context['links'] = sorted(links, key=lambda x: x.get('name'))
        return context


class BaseListView(ModelMixin, ListView):
    template_name = os.path.join("base", "list.html")
    paginate_by = 20

    def get_queryset(self):
        model = self.get_model_class()
        return model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.queryset = self.get_queryset()
        model = self.get_model_class()
        filters = model.get_filterset_class()(self.request.GET, queryset=self.queryset)
        context['create'] = f"/create/{self.kwargs['app']}/{self.kwargs['model']}/"
        context['filters'] = filters
        context['meta'] = model._meta
        context['model'] = model
        object_list = filters.qs
        p = Paginator(object_list, self.paginate_by)

        page_str = self.request.GET.get('page')
        try:
            page = p.page(page_str)
        except PageNotAnInteger:
            # gets first page
            page = p.page(1)
        except EmptyPage:
            # gets last page
            page = p.page(p.num_pages)

        context['object_list'] = page
        context['paginator'] = p
        context['is_paginated'] = True
        context['page_obj'] = page
        return context


class BaseCreateView(ModelMixin, CreateView):
    template_name = os.path.join("base", "create.html")

    def get_success_url(self):
        return reverse(
            'update', 
            kwargs={
                'app': self.kwargs['app'],
                'model': self.kwargs['model'],
                'id': self.object.pk,
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.get_model_class()._meta.verbose_name.title()
        return context

    def get_form_class(self):
        model = self.get_model_class()
        return model.get_form()

    def form_valid(self, form):
        resp = super().form_valid(form)
        model = self.get_model_class()

        if hasattr(model, 'form_valid'):
            model.form_valid(form, self.object)
        return resp 


class BaseUpdateView(ModelMixin, UpdateView):
    template_name = os.path.join("base", "update.html")

    def get_object(self, **kwargs):
        model = self.get_model_class()
        try:
            return model.objects.get(pk=self.kwargs['id'])
        except Exception as e:
            raise Http404()

    def get_success_url(self):
        return reverse(
            'update', 
            kwargs={
                'app': self.kwargs['app'],
                'model': self.kwargs['model'],
                'id': self.object.pk,
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.get_model_class()._meta.verbose_name.title()
        context['create'] = f"/create/{self.kwargs['app']}/{self.kwargs['model']}/"
        context['list'] = f"/list/{self.kwargs['app']}/{self.kwargs['model']}/"
        context['dashboard'] = self.get_model_class().dashboard_template
        try:
            additional_context = self.get_object().dashboard_context()
            context.update(additional_context)
        except NotImplementedError:
            pass 
        return context

    def get_form_class(self):
        model = self.get_model_class()
        return model.get_form(is_update=True)

    def form_valid(self, form):
        resp = super().form_valid(form)
        model = self.get_model_class()
        obj = self.get_object()
        if hasattr(model, 'form_valid'):
            model.form_valid(form, obj)
            
        return resp


class BaseDeleteView(DeleteView):
    template_name = os.path.join("base", "delete.html")


def get_child_table_fields(request, app=None, model=None):
    m = apps.get_model(app_label=app,model_name=model)
    return JsonResponse({
        'properties': child_table_fields(m),
        'update_read_only': hasattr(m, 'update_read_only') and m.update_read_only
    })

def get_child_table_content(request, app=None, model=None, parent_id=None):
    m = apps.get_model(app_label=app,model_name=model)
    qs = m.objects.filter(parent__pk=parent_id)
    data = []
    for child in qs:
        row = {}
        for fieldname in m.field_order:
            name = fieldname
            value = getattr(child, name)
            if isinstance(value, models.Model):
                row[name + "_id"] = value.pk
                row[name] = str(value)
            else:
                row[name] = value
        data.append(row)
    return JsonResponse({'data': data})


def get_model_items(request, app_name=None, model_name=None):
    model = apps.get_model(app_label=app_name, model_name=model_name)
    filter_dict = {}
    try:
        args = json.loads(request.body)
    except:
        args = {}
    
    or_queries = None
    if args.get('filters'):
        filters = json.loads(args['filters']) if type(args['filters']) == str else args['filters']
        and_filters = {}
        for k, v in filters.items():
            if k.startswith('or__'):
                if not or_queries:
                    or_queries = Q(**{k[4:] :  v})
                else:
                    or_queries.add(Q(**{k[4:] :  v}), Q.OR)
            else:
                and_filters[k] = v
        filter_dict.update(and_filters)
        
    qs = model.objects.all()
    if filter_dict:
        qs = model.objects.filter(**filter_dict)
        if or_queries:
            qs = qs.filter(or_queries)
    return JsonResponse({'data': [(i.pk, str(i)) for i in qs]})

def get_token_for_current_user(request):
    if not request.user.is_anonymous:
        token, _ = Token.objects.get_or_create(user=request.user)
        return JsonResponse({'token': token.key})

    csrf_token = get_token(request)
    
    return JsonResponse({
        'detail': "The request's user is not signed in",
        'token': '',
        'csrf': csrf_token
        })
