from rest_framework import serializers
from .models import ContactRequest, Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    work_slug = serializers.SlugRelatedField(source='work', slug_field='slug', read_only=True)

    class Meta:
        model = Testimonial
        fields = ('id', 'author', 'author_role', 'text',
                  'avatar_url', 'source_url', 'work_slug', 'created_at')

    def get_avatar_url(self, obj):
        if not obj.avatar:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url


class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ('name', 'contact', 'message', 'source_page')
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'contact': {'required': True, 'allow_blank': False},
            'message': {'required': False, 'allow_blank': True},
            'source_page': {'required': False, 'allow_blank': True},
        }
