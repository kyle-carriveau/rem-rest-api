import django_filters
from .models import Lease

class LeaseFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")  # Case-insensitive filter
    start_date = django_filters.DateFilter(field_name="start_date", lookup_expr="gte")  # Greater than or equal to
    end_date = django_filters.DateFilter(field_name="end_date", lookup_expr="lte")  # Less than or equal to

    class Meta:
        model = Lease
        fields = ["status", "start_date", "end_date"]