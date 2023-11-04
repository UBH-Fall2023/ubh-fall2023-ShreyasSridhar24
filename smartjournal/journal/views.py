from typing import Any
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse
from django.contrib import messages

from smartjournal.journal.forms import JournalForm
from smartjournal.journal.models import Journal

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
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**args, **kwargs)
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Added journal entry.')
        return reverse('journal_add')