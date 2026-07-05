from rest_framework.views import APIView
from rest_framework.response import Response

from .models import SiteSettings
from .serializers import SiteSettingsSerializer


class SiteSettingsView(APIView):
    def get(self, request):
        obj = SiteSettings.load()
        serializer = SiteSettingsSerializer(obj, context={'request': request})
        return Response(serializer.data)
