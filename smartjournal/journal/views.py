from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

# Create your views here.

class JournalAddView(LoginRequiredMixin, FormView):
    form_class = JournalForm
