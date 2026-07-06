from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL-часть', unique=True, blank=True)
    short_description = models.CharField('Короткое описание', max_length=300, blank=True)
    description = models.TextField('Полное описание', blank=True)
    includes = models.TextField('Что входит', blank=True,
                                 help_text='Каждый пункт с новой строки')
    cover = models.ImageField('Обложка', upload_to='services/', blank=True)
    price_from = models.DecimalField('Цена от, ₽', max_digits=10, decimal_places=0,
                                       null=True, blank=True)
    duration = models.CharField('Длительность', max_length=100, blank=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=False) or 'service'
        super().save(*args, **kwargs)

    def get_includes_list(self):
        return [line.strip() for line in self.includes.splitlines() if line.strip()]

    def __str__(self):
        return self.title


class PriceItem(models.Model):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='price_items', verbose_name='К услуге',
                                 help_text='Оставьте пустым — попадёт в общий прайс')
    title = models.CharField('Позиция', max_length=200)
    price = models.DecimalField('Цена, ₽', max_digits=10, decimal_places=0)
    unit = models.CharField('Единица', max_length=50, blank=True,
                             help_text='Например: за час, за фото, за пакет')
    note = models.CharField('Примечание', max_length=300, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Прайс-позиция'
        verbose_name_plural = 'Прайс'
        ordering = ['order', 'title']

    def __str__(self):
        return f'{self.title} — {self.price} ₽'
