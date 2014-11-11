# -*- coding: utf-8 -*-
from django import template
from django.db import models
register = template.Library()

@register.filter
def getitem(dictionary, key):
    if dictionary:
        return dictionary.get(key)

@register.filter
def verbose_name(obj, key):
    return obj._meta.get_field_by_name(key)[0].verbose_name

@register.filter
def help_text(obj, key):
    return obj._meta.get_field_by_name(key)[0].help_text

@register.filter
def get_value(obj, key):
    return swedify(getattr(obj, key),
                   obj._meta.get_field_by_name(key)[0])


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
