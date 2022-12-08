# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from base.model_utils import build_layout, child_table_fields, parse_form_data_for_child
from crispy_forms.layout import Layout, HTML, Submit
from crispy_forms.helper import FormHelper
from django_filters import FilterSet
from django.apps import apps
import json
import urllib

from django import forms


roles = [("admin", "Admin"),
        ("artisan", "Artisan"),
        ("operator","Operator")]

class BaseModel(models.Model):
    home_visible = True
    class Meta:
        abstract =True
    filter_fields = {}
    list_fields = []
    form_props = {}
    field_order = []
    script = ""
    dashboard_template = ""

    def dashboard_context(self):
        raise NotImplementedError()

    def make_children(self, form):
        if not self.child_table_fields:
            return 
        
        for name in self.child_table_fields:
            field_name = [f for f in self.field_order if name in f][0].split(":")[-1]
            child_app, child_name = field_name.split('.')
            child_model = apps.get_model(child_app, child_name)
            parentfield = child_model.parent 
            child_model.objects.filter(parent=self).delete()
            data_field = name
            if not form.cleaned_data.get(data_field):
                return
            
            data = json.loads(urllib.parse.unquote(form.cleaned_data[data_field]))
            field_data = child_table_fields(child_model)

            for row in data:
                child_instance = child_model(
                    parent=self,
                    **parse_form_data_for_child(self, row, field_data)
                )
                
                child_instance.save()
            

    @property
    def child_table_fields(self):
        return [f.split('.')[1] for f in self.field_order if isinstance(f, str) and '.' in f]


    @staticmethod
    def form_valid(form, obj):
        obj.make_children(form)

    @classmethod
    def get_filterset_class(cls):
        meta = type('Meta', 
                    (), 
                    dict(model=cls,
                        fields=cls.filter_fields)
                    )
        return type(cls._meta.model_name + "_filters", (FilterSet, ), {'Meta': meta})

    @classmethod
    def get_form(cls, is_update=False):
        from base.forms import InputMixin
        
        fields = [f for f in cls.field_order if f not in ["column_break", "section_break"] and isinstance(f, str) and ":" not in f]
        child_table_fields = [f.split('.')[1] for f in cls.field_order if isinstance(f, str) and '.' in f]
        
        meta = type('Meta', tuple(), {
            'model': cls,
            'fields':  fields + child_table_fields
        })
        
        def form_init(self, *args, **kwargs):
            super(self.__class__, self).__init__(*args, **kwargs)            
            if hasattr(cls, "read_only_fields") and is_update:
                for field in self.fields:
                    if not field in cls.read_only_fields: continue                    
                    field = self.fields.get(field)
                    if isinstance(field.widget, forms.widgets.Select):
                        field.widget.attrs['class'] = field.widget.attrs['class'] + ' read-only' 
                    field.widget.attrs['readonly'] = 'readonly' 
            
            self.helper = FormHelper()
            self.helper.layout = build_layout(cls.field_order)
            if hasattr(cls, 'script') and cls.script:
                self.helper.layout.append(HTML('<script>{% include "' + cls.script + '" %}</script>'))
                
            
            self.helper.add_input(Submit('submit', 'Submit'))
        
        form_params = {
            '__init__': form_init,
            'Meta': meta
        }

        form_params.update({f: forms.CharField(widget=forms.HiddenInput, required=False) for f in child_table_fields})

        if hasattr(cls, 'clean_form'):
            form_params['clean'] = cls.clean_form
        
        form = type(f'{cls._meta.model_name}_form',
                    (InputMixin, forms.ModelForm,),
                    form_params)

        return form

    def get_filters(self):
        pass


class Account(User):
    """
    Model that represents any user on the site.
    Inherits from the user class and its functionality, 
    adds the role field to segregate access to different areas within the application.
    """

    role = models.CharField(max_length=128, choices= roles)

    def __str__(self):
        return self.username + " -> " + self.role

