import requests
from django.conf import settings

class QuranAPI:
    BASE = 'https://api.alquran.cloud/v1'

    @staticmethod
    def get_ayah(surah: int, ayah: int):
        """
        Returns a dict with fields: text, juz, hizbQuarter, page, etc.
        """
        # /ayah/{surah}:{ayah}
        url = f"{QuranAPI.BASE}/ayah/{surah}:{ayah}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        if data['status'] != 'OK':
            raise Exception("API error: " + data.get('data', ''))
        return data['data']
