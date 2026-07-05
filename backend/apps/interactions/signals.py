from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.services import notify
from .models import ContactRequest, Testimonial


@receiver(post_save, sender=ContactRequest)
def notify_new_contact_request(sender, instance, created, **kwargs):
    if not created:
        return
    subject = f'Новая заявка от {instance.name}'
    body = (
        f'Имя: {instance.name}\n'
        f'Контакт: {instance.contact}\n'
        f'Сообщение: {instance.message or "—"}\n'
        f'Со страницы: {instance.source_page or "—"}'
    )
    telegram = (
        f'<b>Новая заявка</b>\n\n'
        f'<b>Имя:</b> {instance.name}\n'
        f'<b>Контакт:</b> {instance.contact}\n'
        f'<b>Сообщение:</b> {instance.message or "—"}'
    )
    notify(subject, body, telegram)


@receiver(post_save, sender=Testimonial)
def notify_new_testimonial(sender, instance, created, **kwargs):
    if not created:
        return
    subject = f'Новый отзыв от {instance.author}'
    body = (
        f'Автор: {instance.author}\n'
        f'Текст: {instance.text}\n\n'
        f'Отзыв ждёт модерации в админке.'
    )
    telegram = (
        f'<b>Новый отзыв</b>\n\n'
        f'<b>{instance.author}:</b>\n{instance.text}\n\n'
        f'<i>Ждёт модерации</i>'
    )
    notify(subject, body, telegram)
