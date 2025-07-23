import json
from django.core.management.base import BaseCommand
from quran.models import Juz, Hizb, Quarter, Surah, Ayah

class Command(BaseCommand):
    help = 'Load Qur’an data (surah, ayah, juz, hizb, quarter, page) from JSON'

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str, help='Path to quran.json file')

    def handle(self, *args, **options):
        path = options['json_path']
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # إنشاء Juz, Hizb, Quarter
        # أولاً نعدّل لو JSON فيه أكثر من حزبيْن لكل جزء (غالب ربعان)
        max_juz = max(verse['meta']['juz'] for verse in data['verses'])
        for i in range(1, max_juz + 1):
            Juz.objects.get_or_create(number=i)
            # لكل Juz حزبين متتالين
            for hizb_no in [(i-1)*2 + 1, (i-1)*2 + 2]:
                hz, _ = Hizb.objects.get_or_create(number=hizb_no, juz_id=i)
                # لكل حزب رُبعين داخلَيّاً
                for q_no in [1, 2]:
                    Quarter.objects.get_or_create(hizb=hz, number=q_no)

        # استيراد Surahs و Ayahs
        for verse in data['verses']:
            meta = verse['meta']
            surah_num = meta['chapter']
            ayah_num  = meta['verse']
            juz_no    = meta['juz']
            hizb_no   = meta['hizb']
            rub_no    = meta['hizb_quarter']  # رُبع داخل الحزب
            page_no   = meta['page']

            # أنشئ السورة إذا مش موجودة
            surah, _ = Surah.objects.get_or_create(
                number=surah_num,
                defaults={'name': data['chapters'][surah_num-1]['name_simple']}
            )
            juz     = Juz.objects.get(number=juz_no)
            hizb    = Hizb.objects.get(number=hizb_no)
            quarter = Quarter.objects.get(hizb=hizb, number=rub_no)

            # أنشئ أو حدّث الآية
            Ayah.objects.update_or_create(
                surah=surah,
                number=ayah_num,
                defaults={
                    'juz': juz,
                    'hizb': hizb,
                    'quarter': quarter,
                    'page_number': page_no,
                    'page_half': 'TOP',  # افتراضيّاً نص الصفحة الأعلى
                }
            )

        self.stdout.write(self.style.SUCCESS('✅ Qur’an data loaded successfully.'))
