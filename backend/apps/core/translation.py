from modeltranslation.translator import register, TranslationOptions
from .models import SiteSettings


@register(SiteSettings)
class SiteSettingsTranslation(TranslationOptions):
    fields = ('tagline', 'about_text', 'contact_heading',
              'site_title', 'site_description')
