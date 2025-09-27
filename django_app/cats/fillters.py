import django_filters
from rest_framework import filters
from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


class FilAvailableCatFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get("available") == "true":
            return queryset.filter(Q(missions__isnull=True) | Q(missions__complete=True))
        elif request.query_params.get("available") == "false":
            return queryset.filter(Q(missions__isnull=False) & Q(missions__complete=False))

        return queryset