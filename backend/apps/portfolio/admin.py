from io import StringIO

from django.contrib import admin, messages
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from .models import Category, Work, Photo


TRANSLATION_MEDIA_JS = (
    'modeltranslation/js/force_jquery.js',
    'https://ajax.googleapis.com/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js',
    'modeltranslation/js/tabbed_translation_fields.js',
)
TRANSLATION_MEDIA_CSS = {
    'screen': ('modeltranslation/css/tabbed_translation_fields.css',)
}


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0
    fields = ('image', 'yandex_path', 'order')
    ordering = ('order',)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('title', 'order')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)

    class Media:
        js = TRANSLATION_MEDIA_JS
        css = TRANSLATION_MEDIA_CSS


@admin.register(Work)
class WorkAdmin(TranslationAdmin):
    list_display = (
        'title', 'category', 'shot_date', 'photos_count',
        'is_published', 'order', 'sync_button',
    )
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'order')
    inlines = [PhotoInline]
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'category', 'description', 'shot_date')}),
        ('Медиа', {'fields': ('cover', 'yandex_folder')}),
        ('Публикация', {'fields': ('is_published', 'order')}),
    )
    actions = ['sync_from_yandex']

    def photos_count(self, obj):
        return obj.photos.count()
    photos_count.short_description = 'Фото'

    def sync_button(self, obj):
        if not obj.yandex_folder:
            return format_html('<span style="color:#999">—</span>')
        url = reverse('admin:portfolio_work_sync', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" '
            'style="background:#417690;color:white;padding:6px 12px;'
            'border-radius:4px;text-decoration:none;font-weight:500;" '
            'onclick="return confirm(\'Начать синхронизацию? Это может занять несколько минут.\');">'
            '⬇ Синхр. с Диска</a>',
            url
        )
    sync_button.short_description = 'Яндекс.Диск'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                '<int:pk>/sync-yandex/',
                self.admin_site.admin_view(self.sync_yandex_view),
                name='portfolio_work_sync',
            ),
        ]
        return custom + urls

    def sync_yandex_view(self, request, pk):
        work = self.get_object(request, pk)
        if not work:
            messages.error(request, 'Работа не найдена')
            return HttpResponseRedirect(reverse('admin:portfolio_work_changelist'))
        if not work.yandex_folder:
            messages.warning(request, f'{work.title}: папка на Диске не указана')
            return HttpResponseRedirect(reverse('admin:portfolio_work_change', args=[pk]))

        out = StringIO()
        try:
            call_command('sync_yandex', work=work.slug, stdout=out)
            output = out.getvalue().strip()
            last_line = output.splitlines()[-1] if output else 'готово'
            messages.success(request, f'{work.title}: {last_line}')
        except Exception as e:
            messages.error(request, f'{work.title}: {e}')

        return HttpResponseRedirect(reverse('admin:portfolio_work_change', args=[pk]))

    @admin.action(description='Синхронизировать с Яндекс.Диска')
    def sync_from_yandex(self, request, queryset):
        for work in queryset.exclude(yandex_folder=''):
            out = StringIO()
            try:
                call_command('sync_yandex', work=work.slug, stdout=out)
                output = out.getvalue().strip()
                last_line = output.splitlines()[-1] if output else 'готово'
                messages.success(request, f'{work.title}: {last_line}')
            except Exception as e:
                messages.error(request, f'{work.title}: {e}')

    class Media:
        js = TRANSLATION_MEDIA_JS
        css = TRANSLATION_MEDIA_CSS