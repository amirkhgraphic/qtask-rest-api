from django_filters import rest_framework as filters

from .models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = [
            'phone',
            'is_active',
            'is_staff',
            'is_superuser',
        ]
