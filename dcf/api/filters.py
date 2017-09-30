import django_filters
from rest_framework import filters

from dcf.models import Item


class ItemFilter(filters.FilterSet):
    description = django_filters.CharFilter(name="description", lookup_expr='icontains')

    class Meta:
        model = Item
        fields = ['description', ]