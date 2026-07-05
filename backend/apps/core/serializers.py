from rest_framework import serializers
from .models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    hero_image_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        exclude = ('id', 'hero_image', 'watermark_image',
                   'watermark_enabled', 'watermark_position',
                   'watermark_opacity', 'watermark_size')

    def get_hero_image_url(self, obj):
        if not obj.hero_image:
            return None
        request = self.context.get('request')
        url = obj.hero_image.url
        return request.build_absolute_uri(url) if request else url
