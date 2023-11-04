from django import forms
from django.forms import ModelForm

from smartjournal.journal.models import Journal

class JournalForm(ModelForm):
    class Meta:
        model = Journal