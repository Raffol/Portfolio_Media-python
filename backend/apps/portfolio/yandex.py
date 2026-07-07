import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

API_BASE = 'https://cloud-api.yandex.net/v1/disk'


class YandexDiskError(Exception):
    """Общая ошибка API Яндекс.Диска."""


class YandexDiskClient:
    def __init__(self, token: str | None = None):
        self.token = token or settings.YANDEX_DISK_TOKEN
        if not self.token:
            raise YandexDiskError('YANDEX_DISK_TOKEN не задан в settings')
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def _get(self, url, **kwargs):
        try:
            response = requests.get(url, headers=self.headers, timeout=15, **kwargs)
        except requests.RequestException as e:
            raise YandexDiskError(f'Сетевая ошибка: {e}') from e

        if response.status_code == 401:
            raise YandexDiskError('Токен невалиден. Получите новый на oauth.yandex.ru')
        if response.status_code == 404:
            raise YandexDiskError(
                f'Путь не найден: {kwargs.get("params", {}).get("path", url)}'
            )
        response.raise_for_status()
        return response.json()

    def list_folder(self, path: str, limit: int = 1000) -> list[dict]:
        data = self._get(
            f'{API_BASE}/resources',
            params={'path': path, 'limit': limit, 'sort': 'name'},
        )
        items = data.get('_embedded', {}).get('items', [])
        return [i for i in items if i.get('type') == 'file']

    def get_download_url(self, path: str) -> str:
        data = self._get(f'{API_BASE}/resources/download', params={'path': path})
        return data['href']

    def download(self, path: str) -> bytes:
        url = self.get_download_url(path)
        try:
            response = requests.get(url, timeout=120)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise YandexDiskError(f'Ошибка скачивания {path}: {e}') from e
