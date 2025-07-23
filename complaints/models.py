from django.db import models
from django.conf import settings

class Complaint(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="المستخدم"
    )
    text = models.TextField(
        verbose_name="نص الشكوى"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )

    def __str__(self):
        # لعرض مختصر في لوحة الإدارة
        return f"شكوى #{self.id} من {self.student}"
    
    class Meta:
        verbose_name = "شكوى"
        verbose_name_plural = "الشكاوى"
        ordering = ['-created']
