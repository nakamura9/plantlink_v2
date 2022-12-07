from django import forms
from django.contrib.auth import authenticate
from base.models import Account
from django.contrib.auth import login as auth_login
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
import json


class InputMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            fieldname = field
            field = self.fields.get(field)
            field.widget.attrs['class'] = " "
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 4
            if isinstance(field, forms.models.ModelChoiceField):
                if isinstance(field.widget, forms.widgets.HiddenInput):
                    continue
                field.widget.attrs['data-model'] = field.queryset.model.__name__
                field.widget.attrs['data-app'] = field.queryset.model._meta.app_label
                if isinstance(field, forms.ModelMultipleChoiceField):
                    field.widget.attrs['class'] += " search-widget multiple"
                else:
                    field.widget.attrs['class'] += " search-widget"
                if hasattr(self, 'select_3_filters'):
                    filters = self.select_3_filters.get(fieldname)
                    if filters:                    
                        field.widget.attrs['data-filters'] = json.dumps(filters)


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("username", "password")
        self.helper.add_input(Submit("submit", "Submit"))

    def clean(self):
        cleaned = super().clean()
        user= authenticate(username=cleaned['username'], password=cleaned['password'])
        if not user:
            raise forms.ValidationError("Cannot authenticate user")

# class BaseModelForm(forms.ModelForm):
#     class Meta:
#         model = Modelname
#         fields = fields 
#     

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'email', 'is_superuser', 'first_name', 'last_name', 'role','password1', 'password2')

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user