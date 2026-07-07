from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.portfolio'
    verbose_name = 'Портфолио'

    def ready(self):
        from . import signals  # noqa
