# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from base.model_utils import build_layout
from crispy_forms.layout import Layout, HTML, Submit
from crispy_forms.helper import FormHelper
from django_filters import FilterSet

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

