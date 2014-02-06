# -*- coding: utf-8 -*-
from django import template
from django.db import models
register = template.Library()

@register.filter
def getitem(dictionary, key):
    return dictionary.get(key)

@register.filter
def swedify(val, field):
    if isinstance(val, bool):
        return "Ja" if val else "Nej"
    elif val is None:
        return "[Inget värde angett]"
    elif isinstance(field, models.ManyToManyField):
        return ", ".join([str(x) for x in val.all()])
    elif hasattr(field, 'choices'):
        # lookup if field has choices, and if so look up val in choices
        d = dict(field.choices)
        if val in d:
            return d[val]
        else:
            return val
    else:
        return val
