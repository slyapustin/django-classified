"""
Bootstrap 5 form rendering.

Vendored to replace django-bootstrap-form, whose ``bootstrapform.meta`` module
imports ``distutils`` at load time. distutils was removed from the standard
library in Python 3.12 (PEP 632), so on 3.12+ that import only resolves when
setuptools happens to be installed and its vendored shim is on the path —
meaning a stock ``python:3.12``/``3.13`` environment could not start the app at
all. Upstream's last release was 3.4, in March 2018, and it emitted Bootstrap 3
markup regardless.

Only the plain ``bootstrap`` filter is provided; the ``bootstrap_inline`` and
``bootstrap_horizontal`` variants were never used here. The library name is kept
as ``bootstrap`` so existing ``{% load i18n bootstrap %}`` template overrides
keep working unchanged.

Bootstrap 5 wants a different class per widget family — ``form-select`` for
selects, ``form-check-input`` for checkboxes and radios, ``form-control`` for
everything else — so unlike the Bootstrap 3 original this cannot apply one class
to every field.
"""
from django import forms
from django import template
from django.template.loader import get_template

register = template.Library()

FIELD_TEMPLATE = 'django_classified/forms/field.html'
FORM_TEMPLATE = 'django_classified/forms/form.html'
FORMSET_TEMPLATE = 'django_classified/forms/formset.html'

CONTROL_CLASS = 'form-control'
SELECT_CLASS = 'form-select'
CHECK_CLASS = 'form-check-input'
INVALID_CLASS = 'is-invalid'


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


@register.filter
def is_select(field):
    # RadioSelect and CheckboxSelectMultiple subclass Select but must not get
    # form-select: they render as groups of individual inputs.
    return (
        isinstance(field.field.widget, forms.Select)
        and not is_radio(field)
        and not is_multiple_checkbox(field)
    )


def widget_class(field):
    """Return the Bootstrap 5 class appropriate to this field's widget."""
    if is_checkbox(field) or is_radio(field) or is_multiple_checkbox(field):
        return CHECK_CLASS

    if is_select(field):
        return SELECT_CLASS

    # Bootstrap 5 styles file inputs with form-control, unlike Bootstrap 3.
    return CONTROL_CLASS


def add_widget_classes(field):
    """Add the widget's Bootstrap class, plus is-invalid when the field errored."""
    wanted = [widget_class(field)]

    if field.errors:
        wanted.append(INVALID_CLASS)

    attrs = field.field.widget.attrs
    classes = attrs.get('class', '').split()

    # Widget attrs live on the form field, which outlives a single render, so
    # appending unconditionally would accumulate duplicates every time a form is
    # rendered more than once per page.
    for name in wanted:
        if name not in classes:
            classes.append(name)

    if classes:
        attrs['class'] = ' '.join(classes)


@register.filter
def bootstrap(element):
    """Render a form, formset or bound field using Bootstrap 5 markup."""
    if isinstance(element, forms.BoundField):
        add_widget_classes(element)
        return get_template(FIELD_TEMPLATE).render({'field': element, 'form': element.form})

    if hasattr(element, 'management_form'):
        for form in element.forms:
            for field in form.visible_fields():
                add_widget_classes(field)

        return get_template(FORMSET_TEMPLATE).render({'formset': element})

    for field in element.visible_fields():
        add_widget_classes(field)

    return get_template(FORM_TEMPLATE).render({'form': element})
