import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    payment_date = django_filters.DateFilter(field_name="payment_date", lookup_expr="exact")
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Payment
        fields = ["payment_date", "min_amount", "max_amount"]