import django_filters
from .models import Food

class FoodFilter(django_filters.FilterSet):
    turi = django_filters.CharFilter(field_name='turi', lookup_expr='exact')

    class Meta:
        model = Food
        fields = ['turi']