from typing import Any
import os
import openai
from django.shortcuts import get_object_or_404, render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, FormView, DetailView
from django.urls import reverse
from django.contrib import messages

from journal.forms import JournalForm
from journal.models import Journal
import pytesseract
from PIL import Image
# import cv2
import numpy as np

from plotly.offline import plot
from plotly.graph_objs import Scatter

from django.contrib.auth import authenticate, login

import time
# import easyocr
# import speech_recognition as sr
# from gtts import gTTS

from cryptography.fernet import Fernet
key = Fernet.generate_key()
fernet = Fernet(key)

# Create your views here.

class JournalAddView(LoginRequiredMixin, FormView):
# class JournalAddView(FormView):
    model = Journal
    form_class = JournalForm
    template_name = 'journal/add_journal_entry.html'


    # def get_audio():
    #     r = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         audio = r.listen(source)
    #         said = ""
    #         try:
    #             said = r.recognize_google(audio)
    #             print(said)
    #         except Exception as e:
    #             print("Exception: " + str(e))

    #     return said

    def form_valid(self, form):
        form_data = form.cleaned_data
        user = self.request.user
        title = form_data.get('title')
        message = form_data.get('message')
        date = form_data.get('date')
        is_private = form_data.get('is_private')
        image = form_data.get('image')            
        file = form_data.get('file')
        # process data here (image, file, message)
        # image_enc = bytearray(journal_entry.image)
        # for index, values in enumerate(image_enc):
        #     image_enc[index] = values ^ 1
        # image_enc.write(image_enc)
        # image_enc.close()
        reader = easyocr.Reader(['en'])
        image_words = reader.readtext(image, detail=0)
        journal_entry = Journal.objects.create(title = fernet.encrypt(title.encode()), message = fernet.encrypt(message.encode()), date = date, is_private = is_private, image = image, file = file)
        messages.success(self.request, f"Journal entry from {journal_entry.date} saved!")
        return super().form_valid(form)
    
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**args, **kwargs)
    #     return context

    def get(self, request, *args, **kwargs):
        journal_form = JournalForm()
        context = {}
        context['form'] = journal_form
        # context['mic'] = self.get_audio()
        return render(request, self.template_name, context)
    
    def get_success_url(self):
        messages.success(self.request, 'Added journal entry.')
        return reverse('journal-detail', kwargs={'pk': self.pk_hold})
    
class JournalDetailView(DetailView):
    model = Journal
    template_name = 'journal/journal_detail.html'
    openai.api_key = "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"
    print(openai.api_key)

    def test_func(self):
        """ UserPassesTestMixin Tests"""
        # if self.request.user.is_superuser:
        #     return True

        journal_obj = get_object_or_404(Journal, pk=self.kwargs.get('pk'))
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        # allocation_obj = get_object_or_404(Allocation, pk=pk)

        print("kjjhb!")
        journal_obj = get_object_or_404(Journal, pk=pk)
        context["journal"] = journal_obj
        print(context["journal"])
        # completion = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        # messages=[
        #     {"role": "system", "content": "Give me a dictionary of the valence-arousal,anger,happiness,sadness scores of the following sentence on a scale of -1 to 1. \""+journal_obj.message+"\""},
        #     # {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        # ]
        # )
        # data = completion.choices[0].message["content"]

        # context["data"] = data

        completion2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Pretend you are a therapist. Give me some feedback about the next string as if it was a private entry in my journal. \""+journal_obj.message+"\""},
            # {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
        )

        data2 = completion2.choices[0].message["content"]
        context["data2"]= str(data2)
        print(data2)
        return context
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



        # return None
    
class JournalOverview(TemplateView):
    model = Journal
    template_name = 'journal/journal_overview.html'
    openai.api_key = "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"
    print(openai.api_key)

    def test_func(self):
        """ UserPassesTestMixin Tests"""
        # if self.request.user.is_superuser:
        #     return True

        journal_obj = get_object_or_404(Journal, pk=self.kwargs.get('pk'))
        return True

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
class JournalView(TemplateView):
    template_name = 'journal/journal.html'
