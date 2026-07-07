from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile

from apps.core.models import SiteSettings

MAX_SIDE = 2000
JPEG_QUALITY = 85


def process_photo(image_bytes: bytes, filename: str) -> ContentFile:
    """Пережимает до MAX_SIDE, накладывает вотермарк если включён.

    Возвращает ContentFile, готовый к сохранению в ImageField.
    """
    site_settings = SiteSettings.load()

    source = Image.open(BytesIO(image_bytes))
    source = ImageOps.exif_transpose(source)  # учесть EXIF-поворот
    source = source.convert('RGBA')

    if max(source.size) > MAX_SIDE:
        source.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)

    if site_settings.watermark_enabled and site_settings.watermark_image:
        source = _apply_watermark(source, site_settings)

    result = source.convert('RGB')
    output = BytesIO()
    result.save(output, format='JPEG', quality=JPEG_QUALITY, optimize=True)

    name = filename.rsplit('.', 1)[0] + '.jpg'
    return ContentFile(output.getvalue(), name=name)


def _apply_watermark(source: Image.Image, settings) -> Image.Image:
    try:
        watermark = Image.open(settings.watermark_image.path).convert('RGBA')
    except (FileNotFoundError, OSError):
        return source

    target_width = max(int(source.width * float(settings.watermark_size)), 1)
    ratio = target_width / watermark.width
    new_size = (target_width, max(int(watermark.height * ratio), 1))
    watermark = watermark.resize(new_size, Image.LANCZOS)

    opacity = float(settings.watermark_opacity)
    if opacity < 1.0:
        alpha = watermark.split()[3].point(lambda x: int(x * opacity))
        watermark.putalpha(alpha)

    result = source.copy()
    padding = 40
    pos = settings.watermark_position

    if pos == 'tiled':
        step_x = int(watermark.width * 1.5)
        step_y = int(watermark.height * 1.5)
        for y in range(0, source.height, step_y):
            for x in range(0, source.width, step_x):
                result.paste(watermark, (x, y), watermark)
    else:
        positions = {
            'bottom_right': (source.width - watermark.width - padding,
                             source.height - watermark.height - padding),
            'bottom_left':  (padding,
                             source.height - watermark.height - padding),
            'top_right':    (source.width - watermark.width - padding, padding),
            'top_left':     (padding, padding),
            'center':       ((source.width - watermark.width) // 2,
                             (source.height - watermark.height) // 2),
        }
        result.paste(watermark, positions.get(pos, positions['bottom_right']), watermark)

    return result
