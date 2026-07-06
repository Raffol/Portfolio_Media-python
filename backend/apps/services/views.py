from rest_framework import viewsets

from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Service.objects.filter(is_published=True).prefetch_related('price_items')
    serializer_class = ServiceSerializer
