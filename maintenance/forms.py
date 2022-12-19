from django import forms 
from django.contrib.auth import authenticate
from base.models import Account


class ChecklistForm(forms.Form):
    checklist = forms.MultipleChoiceField(choices=[(i, i) for i in range(10000)])
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        account_user = Account.objects.filter(username=cleaned['username']).exists()
        if not account_user:
            raise forms.ValidationError("Only account users can submit checklists")
        user= authenticate(username=cleaned['username'], password=cleaned['password'])
        if not user:
            raise forms.ValidationError("Cannot authenticate user")