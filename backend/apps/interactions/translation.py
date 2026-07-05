from modeltranslation.translator import register, TranslationOptions
from .models import Testimonial


@register(Testimonial)
class TestimonialTranslation(TranslationOptions):
    fields = ('text', 'author_role')
