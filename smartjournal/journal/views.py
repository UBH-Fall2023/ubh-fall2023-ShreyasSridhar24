from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from smartjournal.journal.forms import JournalForm

# Create your views here.

class JournalAddView(LoginRequiredMixin, FormView):
    form_class = JournalForm
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        user = self.request.user
        journal_entry = Journal.objects.create(
            title = form_data.get('title'),
            user = form_data.get('user'),
            message = form_data.get('message'),
            date = form_data.get('date'),
            is_private = form_data.get('is_private'),
        )

        return super().form_valid(form)