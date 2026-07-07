from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Photo
from .watermark import process_photo


@receiver(pre_save, sender=Photo)
def process_photo_on_save(sender, instance, **kwargs):
    """Автоматически пережимает и ставит вотермарк на фото, загруженные в админке.

    Синхронизацию с Диска пропускаем (там уже прошли через process_photo).
    """
    if not instance.image or instance.yandex_path:
        return

    # Проверка: файл на самом деле поменялся, не второе сохранение того же фото
    if instance.pk:
        try:
            old = Photo.objects.get(pk=instance.pk)
            if old.image and old.image.name == instance.image.name:
                return
        except Photo.DoesNotExist:
            pass

    try:
        instance.image.seek(0)
        content = instance.image.read()
    except (AttributeError, ValueError):
        return

    processed = process_photo(content, instance.image.name)
    instance.image.save(processed.name, processed, save=False)
