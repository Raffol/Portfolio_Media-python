from django.db import models

from apps.portfolio.models import Work


class ContactRequest(models.Model):
    name = models.CharField('Имя', max_length=100)
    contact = models.CharField('Контакт', max_length=200,
                                help_text='Телефон, email, ник в соцсетях')
    message = models.TextField('Сообщение', blank=True)
    source_page = models.CharField('Со страницы', max_length=200, blank=True)

    created_at = models.DateTimeField('Дата', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)
    admin_note = models.TextField('Заметка админа', blank=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.created_at:%d.%m.%Y}'


class Testimonial(models.Model):
    author = models.CharField('Автор', max_length=100)
    author_role = models.CharField('Кто', max_length=200, blank=True,
                                     help_text='Например: невеста, клиент, модель')
    text = models.TextField('Текст отзыва')
    avatar = models.ImageField('Аватар', upload_to='testimonials/', blank=True)
    source_url = models.URLField('Ссылка на источник', blank=True)

    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='testimonials', verbose_name='К работе')

    is_approved = models.BooleanField('Одобрено', default=False,
                                        help_text='Не показывается, пока не одобрено')
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f'{self.author} — {self.created_at:%d.%m.%Y}'
