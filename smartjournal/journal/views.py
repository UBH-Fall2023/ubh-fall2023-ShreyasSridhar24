import json
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

import bcrypt

# Create your views here.

<<<<<<< Updated upstream
class JournalAddView(FormView):
# class JournalAddView(FormView):
=======
# class JournalAddView(LoginRequiredMixin, FormView):
class JournalAddView(FormView):
>>>>>>> Stashed changes
    model = Journal
    form_class = JournalForm
    template_name = 'journal/add_journal_entry.html'
    pk_hold = 1
<<<<<<< Updated upstream
    openai.api_key = "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"

=======
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
        image = form_data.get('image')            
        files = form_data.get('file')
        audio = form_data.get("audio")
        if(image):
            image_ = Image.open(image)
            text = pytesseract.image_to_string(image_)
            print(text)
            message = str(text)
=======
        image = form_data.get('image')  
        print(type(image))          
        file = form_data.get('file')
>>>>>>> Stashed changes
        # process data here (image, file, message)
        # image_enc = bytearray(journal_entry.image)
        # for index, values in enumerate(image_enc):
        #     image_enc[index] = values ^ 1
        # image_enc.write(image_enc)
        # image_enc.close()
<<<<<<< Updated upstream
        # reader = easyocr.Reader(['en'])
        # # image_words = reader.readtext(image, detail=0)
        # if(files):
        #     message
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Give me a dictionary in JSON of the valence-arousal,anger,happiness,sadness scores of the following sentence on a scale of -1 to 1. \""+message+"\""},
            # {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
        )
        data = completion.choices[0].message["content"]


        journal_entry = Journal.objects.create(title = fernet.encrypt(title.encode()), message = fernet.encrypt(message.encode()), date = date, is_private = is_private, image = image, files = files, data = data)
=======
        reader = easyocr.Reader(['en'])
        image_words = reader.readtext(image.read(), detail=0)
        journal_entry = Journal.objects.create(title = title, message = fernet.encrypt(message.encode()), date = date, is_private = is_private, image = image, file = file)
>>>>>>> Stashed changes
        self.pk_hold = journal_entry.pk
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
        # journal_obj.title = journal_obj.title.decode()
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
        journal_obj = get_object_or_404(Journal, pk=self.kwargs.get('pk'))
        x_data = [0,1,2,3]
        y_data = [x**2 for x in x_data]
        plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
        context = {}
        context["sample_graph"] = plot_div
        user = journal_obj.user
        context["avg"] = 0
        avg = 0
        avg_n=0
        for m in user.journal_set.all():
            cav=0
            avg_n+=1
            for n in json.loads(m.data):
                cav+=n
            avg+=cav
        context["avg"] == avg/avg_n
        if(context["avg"]<=-0.5):
            print("call therapy!")

            


        return render(request, self.template_name, context)
# class JournalView(TemplateView):
#     template_name = 'journal/journal.html'

# class TherapistAlert():
