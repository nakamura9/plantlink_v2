from django import template
register = template.Library()
from django.shortcuts import reverse


@register.filter
def get_detail(obj):
    meta_name = str(obj.__class__._meta)
    app_name, model_name = meta_name.split('.')
    
    return reverse('update', kwargs={
        'app': app_name,
        'model': model_name,
        'id': obj.pk
        })

@register.filter
def title(value):
    return value.replace("_", " ").title()


@register.filter
def getattribute(obj, attr):
    value = getattr(obj, attr)
    if isinstance(value, str) and len(value) >= 50:
        return value[:47] + '...'
    return value


@register.filter
def subtract(number, other):
    return number - other