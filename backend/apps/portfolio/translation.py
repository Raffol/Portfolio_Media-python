from modeltranslation.translator import register, TranslationOptions
from .models import Category, Work


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('title',)


@register(Work)
class WorkTranslation(TranslationOptions):
    fields = ('title', 'description')
