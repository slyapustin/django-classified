# -*- coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from .models import Item, Group, Profile, Area


class SearchForm(forms.Form):
    area = forms.ModelChoiceField(label=_('Area'), queryset=Area.objects.all(), required=False)
    group = forms.ModelChoiceField(label=_('Group'), queryset=Group.objects.all(), required=False)
    q = forms.CharField(required=False, label=_('Query'),)

    def filter_by(self):
        # TODO search using more than one field
        # TODO split query string and make seaprate search by words
        filters = {}
        if self.cleaned_data['group']:
            filters['group'] = self.cleaned_data['group']

        if self.cleaned_data['area']:
            filters['area'] = self.cleaned_data['area']

        filters['description__icontains'] = self.cleaned_data['q']

        return filters


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'area',
            'group',
            'title',
            'description',
            'price',
            'is_active'
        )


class PhoneWidget(forms.TextInput):
    input_type = 'phone'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'phone',
        )
        widgets = {
            'phone': PhoneWidget
        }
