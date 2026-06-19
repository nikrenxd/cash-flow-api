from django_filters import rest_framework as filters

from cash_flow.apps.statuses.models import Status


class StatusFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Status
        fields = ("name",)
