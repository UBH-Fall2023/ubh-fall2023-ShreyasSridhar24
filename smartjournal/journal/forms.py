import datetime
from django import forms
from django.forms import ModelForm

from journal.models import Journal
class DateInput(forms.DateInput):
    input_type = 'date'

class JournalForm(ModelForm):
    class Meta:
        model = Journal
        exclude = ('data', 'user')
        widgets = {
            "date": DateInput(attrs={'class':'datepicker', 'value': datetime.datetime.now().strftime("%Y-%m-%d")}),
        }
        labels = {
            "message": "What's on your mind?",
            "image": "Upload a picture of your thoughts if that feels easier :)",
            "files": "Or, upload a file with your brain dump.",
            "date": "When are these thoughts from?",
            "audio_file": "Or or, speak your heart out to us and turn it into a digital entry.",
        }
        def __init__(self, *args, **kwargs):
            super(ModelForm, self).__init__(*args, **kwargs)
            self.fields['image'].required = False
            self.fields['file'].required = False
            self.fields['message'].required = False

