from modeltranslation.translator import register, TranslationOptions
from .models import Service, PriceItem


@register(Service)
class ServiceTranslation(TranslationOptions):
    fields = ('title', 'short_description', 'description', 'includes', 'duration')


@register(PriceItem)
class PriceItemTranslation(TranslationOptions):
    fields = ('title', 'unit', 'note')
