from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models import Service, PriceItem


TRANSLATION_MEDIA_JS = (
    'modeltranslation/js/force_jquery.js',
    'https://ajax.googleapis.com/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js',
    'modeltranslation/js/tabbed_translation_fields.js',
)
TRANSLATION_MEDIA_CSS = {
    'screen': ('modeltranslation/css/tabbed_translation_fields.css',)
}


class PriceItemInline(TranslationTabularInline):
    model = PriceItem
    extra = 0


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('title', 'price_from', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PriceItemInline]

    class Media:
        js = TRANSLATION_MEDIA_JS
        css = TRANSLATION_MEDIA_CSS


@admin.register(PriceItem)
class PriceItemAdmin(TranslationAdmin):
    list_display = ('title', 'service', 'price', 'unit', 'order')
    list_filter = ('service',)
    list_editable = ('order',)

    class Media:
        js = TRANSLATION_MEDIA_JS
        css = TRANSLATION_MEDIA_CSS
