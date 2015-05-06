# -*- coding:utf-8 -*-
from django import forms
from .models import Item, Group, Image
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _


class SearchForm(forms.Form):

    group = forms.ModelChoiceField(label=_('Group'), queryset=Group.objects.all(), required=False)
    q = forms.CharField(required=False, label=_('Query'),)

    def filter_by(self):

        # TODO search by more than one field
        # TODO split query string and make seaprate search by words
        filters = {}

        if self.cleaned_data['group'] is not None:
            filters['group'] = self.cleaned_data['group']

        filters['description__icontains'] = self.cleaned_data['q']

        return filters


class ItemCreateEditForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('group', 'title', 'description', 'price', 'phone', 'is_active')


class AdImageForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = ('owner',)


class ProfileForm(forms.ModelForm):

    email = forms.EmailField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('phone', 'email', 'receive_news', )