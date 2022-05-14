from django import forms 
from inventory.models import Machine


class MaintenanceReviewForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
    all_machines = forms.BooleanField(required=False)
    machine = forms.ModelChoiceField(Machine.objects.all(), required=False)


class BreakdownForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
    all_machines = forms.BooleanField(required=False)
    machine = forms.ModelChoiceField(Machine.objects.all(), required=False)


class MaintenancePlanForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
    all_machines = forms.BooleanField(required=False)
    machine = forms.ModelChoiceField(Machine.objects.all(), required=False)


class WeakPointAnalysisForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
    all_machines = forms.BooleanField(required=False)
    machine = forms.ModelChoiceField(Machine.objects.all(), required=False)