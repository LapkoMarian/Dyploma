from django.forms import ModelForm
from django import forms
from .models import Journal


class AddGradeForm(ModelForm):
    class Meta:
        model = Journal
        fields = ['topik', 'rating']
