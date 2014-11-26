# -*- coding: utf-8 -*-
from django import template
from django.db import models
from register.utils import parse_lagrum, format_lagrum, format_link
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

@register.filter(is_safe=True)
def get_value(obj, key):
    if key == 'lagrum':
        parts = parse_lagrum(getattr(obj, key))
        if parts:
            link = list(format_link(*parts))[0]
            if link:
                return "<a href='%s'>%s</a>" % (link, getattr(obj, key))
            else:
                return getattr(obj, key)
    else:
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
