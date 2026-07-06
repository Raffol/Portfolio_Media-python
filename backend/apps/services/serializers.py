from rest_framework import serializers
from .models import Service, PriceItem


class PriceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceItem
        fields = ('title', 'price', 'unit', 'note', 'order')


class ServiceSerializer(serializers.ModelSerializer):
    price_items = PriceItemSerializer(many=True, read_only=True)
    includes_list = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ('slug', 'title', 'short_description', 'description',
                  'includes_list', 'cover_url', 'price_from', 'duration',
                  'price_items', 'order')

    def get_includes_list(self, obj):
        return obj.get_includes_list()

    def get_cover_url(self, obj):
        if not obj.cover:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(obj.cover.url) if request else obj.cover.url
