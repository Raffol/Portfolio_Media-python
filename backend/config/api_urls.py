from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.core.views import SiteSettingsView
from apps.portfolio.views import CategoryViewSet, WorkViewSet
from apps.services.views import ServiceViewSet
from apps.interactions.views import TestimonialListView, ContactRequestCreateView


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('works', WorkViewSet, basename='works')
router.register('services', ServiceViewSet, basename='services')

urlpatterns = [
    path('', include(router.urls)),
    path('settings/', SiteSettingsView.as_view(), name='settings'),
    path('testimonials/', TestimonialListView.as_view(), name='testimonials'),
    path('contact/', ContactRequestCreateView.as_view(), name='contact'),
]
