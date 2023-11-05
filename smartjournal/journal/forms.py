from django import forms
from django.forms import ModelForm

from journal.models import Journal

class JournalForm(ModelForm):
    class Meta:
        model = Journal
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(ModelForm, self).__init__(*args, **kwargs)
            self.fields['image'].required = False
            self.fields['file'].required = False
            self.fields['message'].required = False

