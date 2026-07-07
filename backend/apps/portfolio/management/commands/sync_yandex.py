from django.core.management.base import BaseCommand
from django.db import transaction

from apps.portfolio.models import Work, Photo
from apps.portfolio.yandex import YandexDiskClient, YandexDiskError
from apps.portfolio.watermark import process_photo


IMAGE_MIMES = {'image/jpeg', 'image/jpg', 'image/png', 'image/webp'}


class Command(BaseCommand):
    help = 'Синхронизировать фото из папок Яндекс.Диска в БД'

    def add_arguments(self, parser):
        parser.add_argument('--work', type=str, default=None,
                            help='slug конкретной работы (иначе все)')
        parser.add_argument('--delete-missing', action='store_true',
                            help='Удалить фото, которых больше нет на Диске')
        parser.add_argument('--dry-run', action='store_true',
                            help='Только показать план, ничего не менять')

    def handle(self, *args, **opts):
        try:
            client = YandexDiskClient()
        except YandexDiskError as e:
            self.stderr.write(self.style.ERROR(str(e)))
            return

        works = Work.objects.exclude(yandex_folder='')
        if opts['work']:
            works = works.filter(slug=opts['work'])

        if not works.exists():
            self.stdout.write('Нет работ с указанной папкой Яндекс.Диска')
            return

        totals = {'added': 0, 'kept': 0, 'deleted': 0, 'errors': 0}

        for work in works:
            self.stdout.write(self.style.HTTP_INFO(
                f'\n→ {work.title}  ({work.yandex_folder})'
            ))
            try:
                stats = self.sync_work(client, work, opts)
                for k, v in stats.items():
                    totals[k] += v
            except YandexDiskError as e:
                self.stderr.write(f'  Ошибка: {e}')
                totals['errors'] += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nГотово. Добавлено: {totals["added"]}, '
            f'без изменений: {totals["kept"]}, '
            f'удалено: {totals["deleted"]}, '
            f'ошибок: {totals["errors"]}'
        ))

    def sync_work(self, client, work, opts):
        stats = {'added': 0, 'kept': 0, 'deleted': 0}

        items = client.list_folder(work.yandex_folder)
        items = [i for i in items if (i.get('mime_type') or '').lower() in IMAGE_MIMES]

        existing = {
            p.yandex_path: p
            for p in work.photos.exclude(yandex_path='')
        }
        seen_paths = set()

        for order, item in enumerate(items):
            path = item['path']
            name = item['name']
            seen_paths.add(path)

            if path in existing:
                self.stdout.write(f'  =  {name}')
                stats['kept'] += 1
                continue

            self.stdout.write(f'  +  {name}')
            if opts['dry_run']:
                continue

            try:
                content = client.download(path)
            except YandexDiskError as e:
                self.stderr.write(f'     Не скачалось: {e}')
                continue

            processed = process_photo(content, name)

            with transaction.atomic():
                photo = Photo(work=work, yandex_path=path, order=order)
                photo.image.save(processed.name, processed, save=True)

            stats['added'] += 1

        if opts['delete_missing']:
            to_delete = [p for p in existing.values() if p.yandex_path not in seen_paths]
            for photo in to_delete:
                self.stdout.write(f'  −  {photo.yandex_path}')
                if not opts['dry_run']:
                    photo.image.delete(save=False)
                    photo.delete()
                stats['deleted'] += 1

        return stats
