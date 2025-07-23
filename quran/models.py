from django.db import models

class Juz(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    class Meta:
        ordering = ['number']
    def __str__(self):
        return f"Juz {self.number}"

class Hizb(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    juz = models.ForeignKey(Juz, related_name='hizbs', on_delete=models.CASCADE)
    class Meta:
        ordering = ['number']
    def __str__(self):
        return f"Hizb {self.number} (Juz {self.juz.number})"

class Quarter(models.Model):
    number = models.PositiveSmallIntegerField()
    hizb = models.ForeignKey(Hizb, related_name='quarters', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('hizb', 'number')
        ordering = ['hizb__number', 'number']
    def __str__(self):
        return f"Quarter {self.number} of Hizb {self.hizb.number}"

class Surah(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=200)
    class Meta:
        ordering = ['number']
    def __str__(self):
        return f"{self.name} ({self.number})"

class Ayah(models.Model):
    surah = models.ForeignKey(Surah, related_name='ayahs', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    juz = models.ForeignKey(Juz, related_name='ayahs', on_delete=models.CASCADE)
    hizb = models.ForeignKey(Hizb, related_name='ayahs', on_delete=models.CASCADE)
    quarter = models.ForeignKey(Quarter, related_name='ayahs', on_delete=models.CASCADE)
    page_number = models.PositiveSmallIntegerField()
    page_half = models.CharField(
        max_length=6,
        choices=[('TOP', 'Top half'), ('BOTTOM', 'Bottom half')]
    )
    class Meta:
        unique_together = ('surah', 'number')
        ordering = ['surah__number', 'number']
    def __str__(self):
        return f"{self.surah.name}:{self.number}"
