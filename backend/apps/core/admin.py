from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from modeltranslation.admin import TranslationAdmin

from .models import SiteSettings


class ColorInput(forms.TextInput):
    input_type = 'color'


class SiteSettingsAdminForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'color_bg': ColorInput(),
            'color_text': ColorInput(),
            'color_muted': ColorInput(),
            'color_accent': ColorInput(),
        }


@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslationAdmin):
    form = SiteSettingsAdminForm
    fieldsets = (
        ('Личное', {
            'fields': ('photographer_name', 'tagline', 'about_text', 'hero_image')
        }),
        ('Контакты', {
            'fields': ('phone', 'email', 'contact_heading')
        }),
        ('Соцсети', {
            'fields': ('vk_url', 'instagram_url', 'telegram_url', 'youtube_url')
        }),
        ('Палитра', {
            'fields': ('color_bg', 'color_text', 'color_muted', 'color_accent')
        }),
        ('Водяной знак', {
            'fields': ('watermark_enabled', 'watermark_image', 'watermark_position',
                       'watermark_opacity', 'watermark_size')
        }),
        ('SEO', {
            'fields': ('site_title', 'site_description'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return redirect(reverse('admin:core_sitesettings_change', args=[obj.pk]))

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {'screen': ('modeltranslation/css/tabbed_translation_fields.css',)}
