from rest_framework import viewsets

from .models import Category, Work
from .serializers import CategorySerializer, WorkListSerializer, WorkDetailSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class WorkViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'

    def get_serializer_class(self):
        return WorkDetailSerializer if self.action == 'retrieve' else WorkListSerializer

    def get_queryset(self):
        qs = (Work.objects
              .filter(is_published=True)
              .select_related('category')
              .prefetch_related('photos'))
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs
