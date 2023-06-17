from django.forms import ModelForm
from django import forms
from .models import Journal


class AddGradeForm(ModelForm):
    class Meta:
        model = Journal
        fields = ['topik', 'rating', 'created_at', 'classroom_user']

        widgets = {
            'created_at': forms.widgets.DateInput(attrs={'type': 'hidden'}),
            'classroom_user': forms.TextInput(attrs={'type': 'hidden'}),
        }
