from django.contrib import admin
from .models import Juz, Hizb, Quarter, Surah, Ayah

@admin.register(Juz)
class JuzAdmin(admin.ModelAdmin):
    list_display = ('number',)

@admin.register(Hizb)
class HizbAdmin(admin.ModelAdmin):
    list_display = ('number', 'juz')

@admin.register(Quarter)
class QuarterAdmin(admin.ModelAdmin):
    list_display = ('hizb', 'number')

@admin.register(Surah)
class SurahAdmin(admin.ModelAdmin):
    list_display = ('number', 'name')

@admin.register(Ayah)
class AyahAdmin(admin.ModelAdmin):
    list_display = ('surah', 'number', 'juz', 'hizb', 'quarter', 'page_number', 'page_half')
    list_filter  = ('juz','hizb','quarter','page_half')
    search_fields = ('surah__name','number')
