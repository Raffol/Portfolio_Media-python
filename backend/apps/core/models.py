from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


hex_validator = RegexValidator(r'^#[0-9a-fA-F]{6}$', 'Формат: #RRGGBB')


class SiteSettings(models.Model):
    WATERMARK_POSITIONS = [
        ('bottom_right', 'Снизу справа'),
        ('bottom_left', 'Снизу слева'),
        ('top_right', 'Сверху справа'),
        ('top_left', 'Сверху слева'),
        ('center', 'По центру'),
        ('tiled', 'Плиткой по всей фотке'),
    ]

    # Личная информация
    photographer_name = models.CharField('Имя', max_length=100, default='Ваше имя')
    tagline = models.CharField('Подзаголовок', max_length=200, blank=True,
                                help_text='Например: Фотограф · Иркутск')
    about_text = models.TextField('О себе', blank=True)
    hero_image = models.ImageField('Главное фото', upload_to='hero/', blank=True)

    # Контакты
    phone = models.CharField('Телефон', max_length=30, blank=True)
    email = models.EmailField('Email', blank=True)
    contact_heading = models.CharField(
        'Заголовок блока контактов', max_length=200,
        default='Для связи напишите или позвоните'
    )

    # Соцсети
    vk_url = models.URLField('ВКонтакте', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    telegram_url = models.URLField('Telegram', blank=True)
    youtube_url = models.URLField('YouTube', blank=True)

    # SEO / мета
    site_title = models.CharField('Title сайта', max_length=200, blank=True)
    site_description = models.TextField('Description', blank=True)

    # Палитра
    color_bg = models.CharField('Цвет фона', max_length=7, default='#ffffff',
                                 validators=[hex_validator])
    color_text = models.CharField('Цвет текста', max_length=7, default='#1a1a1a',
                                   validators=[hex_validator])
    color_muted = models.CharField('Приглушённый текст', max_length=7, default='#666666',
                                    validators=[hex_validator])
    color_accent = models.CharField('Акцент', max_length=7, default='#1a1a1a',
                                     validators=[hex_validator],
                                     help_text='Цвет ссылок и активной навигации')

    # Водяной знак
    watermark_enabled = models.BooleanField('Ставить водяной знак', default=False)
    watermark_image = models.ImageField('Логотип', upload_to='watermark/', blank=True,
                                         help_text='PNG с прозрачностью')
    watermark_position = models.CharField('Положение', max_length=20,
                                           choices=WATERMARK_POSITIONS, default='bottom_right')
    watermark_opacity = models.DecimalField('Прозрачность', max_digits=3, decimal_places=2,
                                             default=0.30,
                                             help_text='0.00 — невидимо, 1.00 — непрозрачно')
    watermark_size = models.DecimalField('Размер (% от ширины фото)', max_digits=4,
                                          decimal_places=2, default=0.15,
                                          help_text='0.15 = 15% ширины фотки')

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('Настройки сайта уже существуют.')
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Настройки сайта'
