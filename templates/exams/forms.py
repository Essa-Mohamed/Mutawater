from django import forms
from quran.models import Juz, Hizb, Quarter

class ScopeForm(forms.Form):
    juzs     = forms.ModelMultipleChoiceField(
        queryset=Juz.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="الأجزاء (Juz)"
    )
    hizbs    = forms.ModelMultipleChoiceField(
        queryset=Hizb.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="الأحزاب (Hizb)"
    )
    quarters = forms.ModelMultipleChoiceField(
        queryset=Quarter.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="الأرباع (Quarter)"
    )

    def clean(self):
        cleaned = super().clean()
        if not (cleaned.get('juzs') or cleaned.get('hizbs') or cleaned.get('quarters')):
            raise forms.ValidationError("لازم تختار جزء واحد على الأقل، أو حزب، أو رُبع.")
        return cleaned
