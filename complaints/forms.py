from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['text']
        labels = {
            'text': 'نص الشكوى'
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'اكتب شكواك هنا…'})
        }
