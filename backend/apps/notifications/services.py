import logging
import requests
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_telegram(text: str) -> None:
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        logger.debug('Telegram не настроен, пропускаем уведомление')
        return
    try:
        requests.post(
            f'https://api.telegram.org/bot{token}/sendMessage',
            json={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'},
            timeout=5,
        )
    except requests.RequestException as e:
        logger.error(f'Ошибка отправки в Telegram: {e}')


def notify(subject: str, body: str, telegram_body: str | None = None) -> None:
    """Уведомить фотографа обоими каналами. Ошибки не роняют запрос."""
    if settings.NOTIFY_EMAIL:
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f'Ошибка отправки email: {e}')

    send_telegram(telegram_body or f'<b>{subject}</b>\n\n{body}')
