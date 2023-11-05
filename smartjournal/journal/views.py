from typing import Any
from django.shortcuts import get_object_or_404, render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, FormView
from django.urls import reverse
from django.contrib import messages

from journal.forms import JournalForm
from journal.models import Journal

from plotly.offline import plot
from plotly.graph_objs import Scatter

# Create your views here.

# class JournalAddView(LoginRequiredMixin, FormView):
class JournalAddView(FormView):
    form_class = JournalForm
    template_name = 'journal/add_journal_entry.html'
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        user = self.request.user
        journal_entry = Journal.objects.create(
            title = form_data.get('title'),
            message = form_data.get('message'),
            date = form_data.get('date'),
            is_private = form_data.get('is_private'),
        )

        return super().form_valid(form)
    
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**args, **kwargs)
    #     return context

    def get(self, request, *args, **kwargs):
        journal_form = JournalForm()
        context = {}
        context['form'] = journal_form
        return render(request, self.template_name, context)
    
    def get_success_url(self):
        messages.success(self.request, 'Added journal entry.')
        return reverse('journal-add')
    
class JournalDetailView(TemplateView):
    template_name = 'journal/journal_view.html'
    def test_func(self):
        """ UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        journal_obj = get_object_or_404(Journal, pk=self.kwargs.get('pk'))

        if journal_obj.user == self.request.user:
            return True

        # if journal_obj.projectuser_set.filter(user=self.request.user, role__name='Manager', status__name='Active').exists():
        #     return True

        messages.error(self.request, 'You do not have permission to download all notes.')
    
    def get(self, request, *args, **kwargs):
        x_data = [0,1,2,3]
        y_data = [x**2 for x in x_data]
        plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
        context = {}
        context["sample_graph"] = plot_div
        return render(request, self.template_name, context)

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # pk = self.kwargs.get('pk')
        # allocation_obj = get_object_or_404(Allocation, pk=pk)
        # journal_obj = get_object_or_404(Journal, pk=pk)
        # context["journal"] = journal_obj

        return context
    



