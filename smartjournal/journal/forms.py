import datetime
from django import forms
from django.forms import ModelForm

from journal.models import Journal
class DateInput(forms.DateInput):
    input_type = 'date'

class JournalForm(ModelForm):
    class Meta:
        model = Journal
        fields = '__all__'
        widgets = {
            "date": DateInput(attrs={'class':'datepicker', 'value': datetime.datetime.now().strftime("%Y-%m-%d")}),
        }
        labels = {
            "message": "What's on your mind?",
            "image": "Upload a picture of your thoughts if that feels easier :)",
            "file": "Or, upload a file with your brain dump.",
            "date": "When are these thoughts from?",
        }
        def __init__(self, *args, **kwargs):
            super(ModelForm, self).__init__(*args, **kwargs)
            self.fields['image'].required = False
            self.fields['file'].required = False
            self.fields['message'].required = False

