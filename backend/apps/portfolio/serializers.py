from rest_framework import serializers
from .models import Category, Work, Photo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'title', 'order')


class PhotoSerializer(serializers.ModelSerializer):
    preview_url = serializers.SerializerMethodField()
    full_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('id', 'preview_url', 'full_url', 'width', 'height')

    def _absolute(self, url):
        request = self.context.get('request')
        if request and url and not url.startswith('http'):
            return request.build_absolute_uri(url)
        return url

    def get_preview_url(self, obj):
        if obj.image:
            return self._absolute(obj.image.url)
        return None

    def get_full_url(self, obj):
        if obj.image:
            return self._absolute(obj.image.url)
        return None


class WorkListSerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Work
        fields = ('slug', 'title', 'category', 'shot_date', 'cover_url')

    def get_cover_url(self, obj):
        if not obj.cover:
            return None
        request = self.context.get('request')
        url = obj.cover.url
        return request.build_absolute_uri(url) if request else url


class WorkDetailSerializer(WorkListSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta(WorkListSerializer.Meta):
        fields = WorkListSerializer.Meta.fields + ('description', 'photos')
