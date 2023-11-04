from django import forms
from django.forms import ModelForm

class JournalForm(ModelForm):
    class Meta:
        model = Journal