from django import forms 

class ImportForm(forms.Form):
    file = forms.FileField(required=True)
    type = forms.ChoiceField(choices=(('machines', 'Machines'), ('spares', 'Spares')), required=True)