from django_filters import rest_framework as filters

from .models import KeyValue


class KeyValueFilter(filters.FilterSet):
    parent = filters.ModelChoiceFilter(
        queryset=KeyValue.objects.filter(type=KeyValue.KeyValueTypeChoices.NESTED),
        field_name='parent',
        lookup_expr='exact',
    )

    parent_isnull = filters.BooleanFilter(
        field_name='parent',
        lookup_expr='isnull',
        label='Parent is null'
    )

    class Meta:
        model = KeyValue
        fields = [
            'type',
            'parent',
            'parent_isnull',
        ]
