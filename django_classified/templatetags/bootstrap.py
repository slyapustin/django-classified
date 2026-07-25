"""
Bootstrap 3 form rendering.

Vendored to replace django-bootstrap-form, whose ``bootstrapform.meta`` module
imports ``distutils`` at load time. distutils was removed from the standard
library in Python 3.12 (PEP 632), so on 3.12+ that import only resolves when
setuptools happens to be installed and its vendored shim is on the path —
meaning a stock ``python:3.12``/``3.13`` environment could not start the app at
all. Upstream's last release was 3.4, in March 2018.

Only the plain ``bootstrap`` filter is reimplemented; the ``bootstrap_inline``
and ``bootstrap_horizontal`` variants were never used here. The library name is
kept as ``bootstrap`` so existing ``{% load i18n bootstrap %}`` template
overrides keep working unchanged.
"""
from django import forms
from django import template
from django.template.loader import get_template

register = template.Library()

FIELD_TEMPLATE = 'django_classified/forms/field.html'
FORM_TEMPLATE = 'django_classified/forms/form.html'
FORMSET_TEMPLATE = 'django_classified/forms/formset.html'

INPUT_CLASS = 'form-control'


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


def add_input_class(field):
    """Add Bootstrap's form-control class to the widgets that should carry it."""
    if is_checkbox(field) or is_multiple_checkbox(field) or is_radio(field) or is_file(field):
        return

    attrs = field.field.widget.attrs
    classes = attrs.get('class', '').split()

    # Widget attrs live on the form field, which outlives a single render, so
    # appending unconditionally would accumulate duplicates every time a form is
    # rendered more than once per page.
    if INPUT_CLASS not in classes:
        classes.append(INPUT_CLASS)
        attrs['class'] = ' '.join(classes)


@register.filter
def bootstrap(element):
    """Render a form, formset or bound field using Bootstrap 3 markup."""
    if isinstance(element, forms.BoundField):
        add_input_class(element)
        return get_template(FIELD_TEMPLATE).render({'field': element, 'form': element.form})

    if hasattr(element, 'management_form'):
        for form in element.forms:
            for field in form.visible_fields():
                add_input_class(field)

        return get_template(FORMSET_TEMPLATE).render({'formset': element})

    for field in element.visible_fields():
        add_input_class(field)

    return get_template(FORM_TEMPLATE).render({'form': element})
