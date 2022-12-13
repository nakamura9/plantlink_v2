from django.db import models
from crispy_forms.layout import (Layout, Row, Column, HTML)
from django.apps import apps 
import copy 

'''
Sample layout 
field
field 
column_break
'''


def build_layout(field_order):
    '''Support section breaks later'''
    # 1. Identify sections. represented by rows 
    # 2. Identify columns. represented by columns.
    # if no rows and columns return the array as is 
    # if sections, divide list at section breaks
    # if column breaks, divide section by breaks
    layout = []
    child_table_fields = [f.split('.')[1] for f in field_order if isinstance(f, str) and '.' in f]
    field_order = copy.deepcopy(field_order)

    def get_columns(fields):
        columns = []
        start = 0
        for i, field in enumerate(fields, start=0):
            if field == "column_break":
                columns.append(fields[start:i])
                start = i + 1

        if len(columns) > 0:
            columns.append(fields[start:len(fields)])
            return fields, columns
        
        return fields, columns
    
    sections = []
    start = 0
    for i, field in enumerate(field_order, start=0):
        if field == "section_break":
            sections.append(field_order[start: i])
            start = i + 1

        if isinstance(field, str) and field.startswith("child:"):
            app, model = field[6:].split('.')
            m = apps.get_model(app_label=app,model_name=model)
            field_order[i] = HTML(f"<h5>{m._meta.verbose_name}</h5><div data-app='{app}' data-model='{model}' class='child-table'></div>")



    if len(sections) > 0:
        sections.append(field_order[start:len(field_order)])
        for section in sections:
            fields, columns = get_columns(section)
            if len(columns) > 0:
                css_class = f"col-sm-12 col-md-{int(12 / len(columns))}"
                col_objs = []
                for column in columns:
                    col_objs.append(Column(*column, css_class=css_class))

                layout.append(Row(*col_objs))
            else:
                layout.append(Row(Column(*section, css_class='col-12')))

    else:
        fields, columns = get_columns(field_order)
        if len(columns) > 0:
            css_class = f"col-sm-12 col-md-{int(12 / len(columns))}"
            col_objs = []
            for column in columns:
                col_objs.append(Column(*column, css_class=css_class))

            layout.append(Row(*col_objs))
        else:
            layout.append(Row(Column(*field_order, css_class='col-12')))
    
    layout.extend(child_table_fields)

    return Layout(
        *layout
    )


def child_table_fields(model):
    field_list = []
    field_map = {field.name: field for field in model._meta.fields}
    if not hasattr(model, "field_order"):
        raise Exception("Field order is required for child table")

    def get_options(f):
        if isinstance(f, models.ForeignKey):
            app_name = f.remote_field.model._meta.app_label
            model_name = f.remote_field.model.__name__
            return f"{app_name}.{model_name}"

        if hasattr(f, 'choices') and f.choices:
            return f.choices

        return None

    for fieldname in model.field_order:
        field = field_map.get(fieldname)
        fieldtype = ""
        if isinstance(field, models.DateField):
            fieldtype = 'date'
        elif isinstance(field, models.BooleanField):
            fieldtype = 'bool'
        elif isinstance(field, models.ForeignKey):
            fieldtype = 'link'
        elif isinstance(field, models.DurationField) or \
            isinstance(field, models.TimeField):
            fieldtype = 'time'
        elif isinstance(field, models.FloatField) or \
                isinstance(field, models.DecimalField) or \
                isinstance(field, models.IntegerField):
            fieldtype = 'number'
        elif isinstance(field, models.CharField):
            if hasattr(field, 'choices') and field.choices:
                fieldtype = "select"
            fieldtype = "char"

        elif isinstance(field, models.TextField):
            fieldtype = 'text'

        field_list.append({
            'name': fieldname,
            'label': fieldname.replace('_', ' ').title(),
            'type': fieldtype,
            'options': get_options(field)
        })

    return field_list


def parse_form_data_for_child(model, data, field_data):
    res = {}
    for f in field_data:
        name = f['name']
        if f['type'] == 'link':
            fk_model = apps.get_model(*f['options'].split('.'))
            fk_id = data[name + "_id"]
            print(fk_id)
            fk_instance = fk_model.objects.get(pk=fk_id)
            res[name] = fk_instance
        else:
            res[name] = data[name] 

    print(res)
    return res