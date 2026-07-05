from django.apps import AppConfig


class InteractionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.interactions'
    verbose_name = 'Заявки и отзывы'

    def ready(self):
        from . import signals  # noqa
