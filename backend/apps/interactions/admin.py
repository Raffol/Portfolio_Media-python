from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import ContactRequest, Testimonial


TRANSLATION_MEDIA_JS = (
    'modeltranslation/js/force_jquery.js',
    'https://ajax.googleapis.com/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js',
    'modeltranslation/js/tabbed_translation_fields.js',
)
TRANSLATION_MEDIA_CSS = {
    'screen': ('modeltranslation/css/tabbed_translation_fields.css',)
}


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    list_editable = ('is_processed',)
    readonly_fields = ('name', 'contact', 'message', 'source_page', 'created_at')
    fields = ('name', 'contact', 'message', 'source_page', 'created_at',
              'is_processed', 'admin_note')


@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin):
    list_display = ('author', 'work', 'is_approved', 'created_at', 'order')
    list_filter = ('is_approved',)
    list_editable = ('is_approved', 'order')
    actions = ['approve_selected']

    @admin.action(description='Одобрить выбранные отзывы')
    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)

    class Media:
        js = TRANSLATION_MEDIA_JS
        css = TRANSLATION_MEDIA_CSS
