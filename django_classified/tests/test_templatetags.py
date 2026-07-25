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
    """Bootstrap 5 form rendering, vendored in place of django-bootstrap-form."""

    def render(self, form):
        return Template('{% load bootstrap %}{{ form|bootstrap }}').render(Context({'form': form}))

    def test_wraps_fields_in_mb_3(self):
        html = self.render(ExampleForm())

        self.assertIn('mb-3', html)
        self.assertIn('form-label', html)

    def test_adds_form_control_to_text_and_number_inputs(self):
        form = ExampleForm()
        self.render(form)

        self.assertIn('form-control', form.fields['text'].widget.attrs['class'])
        self.assertIn('form-control', form.fields['number'].widget.attrs['class'])

    def test_select_gets_form_select_not_form_control(self):
        form = ExampleForm()
        self.render(form)

        classes = form.fields['choice'].widget.attrs['class']
        self.assertIn('form-select', classes)
        self.assertNotIn('form-control', classes)

    def test_checkbox_and_radio_get_form_check_input(self):
        form = ExampleForm()
        html = self.render(form)

        for name in ('checkbox', 'radio'):
            classes = form.fields[name].widget.attrs.get('class', '')
            self.assertIn('form-check-input', classes)
            self.assertNotIn('form-control', classes)

        self.assertIn('form-check', html)
        self.assertIn('form-check-label', html)

    def test_file_input_gets_form_control(self):
        # Unlike Bootstrap 3, Bootstrap 5 styles file inputs with form-control.
        form = ExampleForm()
        self.render(form)

        self.assertIn('form-control', form.fields['attachment'].widget.attrs.get('class', ''))

    def test_does_not_duplicate_class_when_rendered_twice(self):
        form = ExampleForm()
        self.render(form)
        self.render(form)

        self.assertEqual(form.fields['text'].widget.attrs['class'].split().count('form-control'), 1)
        self.assertEqual(form.fields['choice'].widget.attrs['class'].split().count('form-select'), 1)

    def test_renders_help_text_with_form_text(self):
        html = self.render(ExampleForm())

        self.assertIn('A hint', html)
        self.assertIn('form-text', html)

    def test_renders_errors_as_invalid_feedback(self):
        bound = ExampleForm(data={})
        html = self.render(bound)

        self.assertIn('invalid-feedback d-block', html)
        self.assertNotIn('has-error', html)
        self.assertNotIn('help-block', html)

    def test_adds_is_invalid_to_errored_field(self):
        bound = ExampleForm(data={})
        self.render(bound)

        self.assertIn('is-invalid', bound.fields['text'].widget.attrs['class'])

    def test_renders_single_bound_field(self):
        html = bootstrap(ExampleForm()['text'])

        self.assertIn('mb-3', html)
        self.assertIn('Text', html)

    def test_renders_formset(self):
        formset_class = inlineformset_factory(Item, Image, fields=('file',), extra=1)
        html = bootstrap(formset_class())

        self.assertIn('TOTAL_FORMS', html)
        self.assertIn('mb-3', html)

    def test_renders_radio_choices(self):
        html = self.render(ExampleForm())

        self.assertIn('form-check', html)
        self.assertIn('form-check-input', html)
        self.assertIn('form-check-label', html)
