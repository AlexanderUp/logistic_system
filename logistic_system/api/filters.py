from django_filters import rest_framework as filters

from cargo.models import Cargo


class CargoFilter(filters.FilterSet):
    max_weight = filters.NumberFilter(field_name='weight', lookup_expr='lte')
    min_weight = filters.NumberFilter(field_name='weight', lookup_expr='gte')

    class Meta:
        model = Cargo
        fields = ['weight']
