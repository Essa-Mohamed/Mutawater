from django.db import models
from django.conf import settings
from quran.models import Ayah, Quarter

class TestSession(models.Model):
    TEST_TYPES = [
        ('SIMILAR', 'Similar verses'),
        ('SIM_RUB', 'Similar + Quarter'),
        ('MIXED', 'Mixed'),
        ('MAP', 'Full mapping'),
    ]
    DIFFICULTY = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]

    student       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tests', on_delete=models.CASCADE)
    test_type     = models.CharField(max_length=10, choices=TEST_TYPES)
    difficulty    = models.CharField(max_length=1, choices=DIFFICULTY)
    num_questions = models.PositiveSmallIntegerField(null=True, blank=True)
    start_time    = models.DateTimeField(auto_now_add=True)
    end_time      = models.DateTimeField(null=True, blank=True)
    score         = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Test #{self.id} ({self.get_test_type_display()})"


class Question(models.Model):
    session            = models.ForeignKey(TestSession, related_name='questions', on_delete=models.CASCADE)
    ayah               = models.ForeignKey(Ayah, on_delete=models.CASCADE)
    selected_quarter   = models.ForeignKey(Quarter, null=True, blank=True, on_delete=models.SET_NULL)
    selected_page      = models.PositiveSmallIntegerField(null=True, blank=True)
    selected_half      = models.CharField(
                            max_length=6,
                            choices=[('TOP','Top half'), ('BOTTOM','Bottom half')],
                            blank=True
                        )
    is_correct         = models.BooleanField(default=False)

    def __str__(self):
        return f"Q{self.id} of Test {self.session.id}"
