from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import Item, Group, Profile, Area


class SearchForm(forms.Form):
    area = forms.ModelChoiceField(label=_('Area'), queryset=Area.objects.all(), required=False)
    group = forms.ModelChoiceField(label=_('Group'), queryset=Group.objects.all(), required=False)
    q = forms.CharField(required=False, label=_('Query'),)

    def get_queryset_filter(self):
        q_filter = Q()

        if self.cleaned_data['group']:
            q_filter &= Q(group=self.cleaned_data['group'])

        if self.cleaned_data['area']:
            q_filter &= Q(area=self.cleaned_data['area'])

        query = self.cleaned_data.get('q', '').strip()
        if query:
            words = query.split()
            for word in words:
                q_filter &= (
                    Q(title__icontains=word) | Q(description__icontains=word)
                )

        return q_filter


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
    input_type = 'tel'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'phone',
        )
        widgets = {
            'phone': PhoneWidget
        }
