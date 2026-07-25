from django import forms
from django.forms import inlineformset_factory
from django.template import Context, Template
from django.test import TestCase

from django_classified.models import Image, Item
from django_classified.templatetags.bootstrap import bootstrap


class ExampleForm(forms.Form):
    text = forms.CharField(label='Text')
    number = forms.DecimalField(label='Number', help_text='A hint')
    choice = forms.ChoiceField(label='Choice', choices=[(1, 'One'), (2, 'Two')])
    radio = forms.ChoiceField(label='Radio', choices=[(1, 'One')], widget=forms.RadioSelect, required=False)
    checkbox = forms.BooleanField(label='Checkbox', required=False)
    attachment = forms.FileField(label='Attachment', required=False)


class BootstrapFilterTestCase(TestCase):
    """Bootstrap 3 form rendering, vendored in place of django-bootstrap-form."""

    def render(self, form):
        return Template('{% load bootstrap %}{{ form|bootstrap }}').render(Context({'form': form}))

    def test_wraps_fields_in_form_group(self):
        html = self.render(ExampleForm())

        self.assertIn('form-group', html)
        self.assertIn('control-label', html)

    def test_adds_form_control_to_text_input(self):
        form = ExampleForm()
        self.render(form)

        self.assertIn('form-control', form.fields['text'].widget.attrs['class'])
        self.assertIn('form-control', form.fields['choice'].widget.attrs['class'])

    def test_skips_form_control_on_checkbox_radio_and_file(self):
        form = ExampleForm()
        self.render(form)

        for name in ('checkbox', 'radio', 'attachment'):
            self.assertNotIn('form-control', form.fields[name].widget.attrs.get('class', ''))

    def test_does_not_duplicate_class_when_rendered_twice(self):
        form = ExampleForm()
        self.render(form)
        self.render(form)

        self.assertEqual(form.fields['text'].widget.attrs['class'].split().count('form-control'), 1)

    def test_renders_help_text_and_errors(self):
        html = self.render(ExampleForm())
        self.assertIn('A hint', html)

        bound = ExampleForm(data={})
        errors = self.render(bound)
        self.assertIn('has-error', errors)
        self.assertIn('help-block', errors)

    def test_renders_single_bound_field(self):
        html = bootstrap(ExampleForm()['text'])

        self.assertIn('form-group', html)
        self.assertIn('Text', html)

    def test_renders_formset(self):
        formset_class = inlineformset_factory(Item, Image, fields=('file',), extra=1)
        html = bootstrap(formset_class())

        self.assertIn('TOTAL_FORMS', html)
        self.assertIn('form-group', html)

    def test_renders_radio_choices(self):
        html = self.render(ExampleForm())

        self.assertIn('class="radio"', html)
