from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import Testimonial
from .serializers import TestimonialSerializer, ContactRequestSerializer


class TestimonialListView(ListAPIView):
    queryset = Testimonial.objects.filter(is_approved=True)
    serializer_class = TestimonialSerializer


class ContactThrottle(AnonRateThrottle):
    scope = 'contact'


class ContactRequestCreateView(CreateAPIView):
    serializer_class = ContactRequestSerializer
    throttle_classes = [ContactThrottle]

    def create(self, request, *args, **kwargs):
        # honeypot: если бот заполнил невидимое поле, делаем вид что всё ок
        if request.data.get('website'):
            return Response({'ok': True}, status=201)
        return super().create(request, *args, **kwargs)
