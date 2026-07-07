from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL-часть', unique=True, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=False) or 'category'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Work(models.Model):
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL-часть', unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    shot_date = models.DateField('Дата съёмки', null=True, blank=True)
    cover = models.ImageField('Обложка', upload_to='covers/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                  related_name='works', verbose_name='Категория')
    yandex_folder = models.CharField(
        'Папка на Яндекс.Диске', max_length=500, blank=True,
        help_text='Например: /portfolio/weddings/ivanovy-2024/'
    )
    is_published = models.BooleanField('Опубликовано', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
        ordering = ['order', '-shot_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=False) or 'work'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Photo(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='photos',
                              verbose_name='Работа')
    image = models.ImageField('Файл', upload_to='photos/', blank=True,
                               width_field='width', height_field='height',
                               help_text='Оставьте пустым, если фото на Яндекс.Диске')
    yandex_path = models.CharField('Путь на Диске', max_length=500, blank=True)
    width = models.PositiveIntegerField('Ширина', default=0)
    height = models.PositiveIntegerField('Высота', default=0)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.work.title} · {self.id}'
