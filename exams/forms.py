# exams/forms.py

from django import forms
from quran.models import Juz, Hizb, Quarter

# Custom fields to provide our Arabic labels per instance
class JuzMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, juz):
        return f"الجزء {juz.number}"

class HizbMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, hizb):
        return f"الحزب {hizb.number}"

class QuarterMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, quarter):
        return f"الربع {quarter.number}"

class ScopeForm(forms.Form):
    juzs = JuzMultipleChoiceField(
        queryset=Juz.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="الأجزاء"
    )
    hizbs = HizbMultipleChoiceField(
        queryset=Hizb.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="الأحزاب"
    )
    quarters = QuarterMultipleChoiceField(
        queryset=Quarter.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="الأرباع"
    )

class TestTypeForm(forms.Form):
    TEST_CHOICES = [
        ('direct', 'سؤال مباشر (آية → موقع)'),
        ('reverse', 'سؤال عكسي (موقع → آية)'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'سهل'),
        ('medium', 'متوسط'),
        ('hard', 'صعب'),
    ]
    NUM_CHOICES = [(i, f"{i} سؤال") for i in (5, 10, 15, 20)]

    test_type = forms.ChoiceField(
        choices=TEST_CHOICES,
        label="نوع الاختبار"
    )
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        label="الصعوبة"
    )
    num_questions = forms.ChoiceField(
        choices=NUM_CHOICES,
        label="عدد الأسئلة"
    )
