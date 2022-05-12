from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


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