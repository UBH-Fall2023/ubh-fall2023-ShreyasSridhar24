# from datetime import datetime
import datetime
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
import easyocr

from skimage import io

# import speech_recognition as sr
# from gtts import gTTS

from cryptography.fernet import Fernet
key = Fernet.generate_key()
fernet = Fernet(key)

import bcrypt

# Create your views here.

# class JournalAddView(LoginRequiredMixin, FormView):
class JournalAddView(FormView):
    model = Journal
    form_class = JournalForm
    template_name = 'journal/add_journal_entry.html'
    pk_hold = 1
    openai.api_key = "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"

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
        files = form_data.get('file')
        audio = form_data.get("audio")
        if(image):
            image_ = Image.open(image)
            text = pytesseract.image_to_string(image_, lang="eng")
            message = str(text)
        # image = form_data.get('image')  
        # print(type(image))          
        file = form_data.get('file')
        # process data here (image, file, message)
        # image_enc = bytearray(journal_entry.image)
        # for index, values in enumerate(image_enc):
        #     image_enc[index] = values ^ 1
        # image_enc.write(image_enc)
        # image_enc.close()
        # reader = easyocr.Reader(['en'])
        # # image_words = reader.readtext(image, detail=0)
        # if(files):
        #     message
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Give me a dictionary in JSON of the valence-arousal,anger,happiness,sadness scores of the following sentence on a scale of -1 to 1, make sure the keys are valence-arousal,anger,happiness and sadness. \""+message+"\""},
            # {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
        )
        data = completion.choices[0].message["content"]


        journal_entry = Journal.objects.create(title = title, message = message, date = date, is_private = is_private, image = image, files = files, data = data)
        # if image:
        #     img = io.imread(image)
        #     reader = easyocr.Reader(['en'])
        #     image_words = reader.readtext(img.read(), detail=0)
        # journal_entry = Journal.objects.create(title = title, message = fernet.encrypt(message.encode()), date = date, is_private = is_private, image = image, file = file)
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

        # completion2 = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        # messages=[
        #     {"role": "system", "content": "Pretend you are a therapist. Give me some feedback about the next string as if it was a private entry in my journal. \""+journal_obj.message+"\""},
        #     # {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        # ]
        # )

        # data2 = completion2.choices[0].message["content"]
        # context["data2"]= str(data2)
        # print(data2)
        return context
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



        # return None
    
class JournalOverview(TemplateView):
    model = Journal
    template_name = 'journal/journal_view.html'
    openai.api_key = "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"
    print(openai.api_key)

    def test_func(self):
        """ UserPassesTestMixin Tests"""
        # if self.request.user.is_superuser:
        #     return True

        # journal_obj = get_object_or_404(Journal, pk=self.kwargs.get('pk'))
        return True

    def get(self, request, *args, **kwargs):
        # journal_obj = get_object_or_404(Journal, pk=self.kwargs.get('pk'))
        context = {}
        user = self.request.user
        context["avg"] = 0
        print(Journal.objects.all())
        avg = 0
        avg_n=0
        listify = []
        streak = 0
        queryset = Journal.objects.all()
        # print(type(list(queryset)))
        queryset = list(queryset)
        for journal in queryset:
            data = journal.data
            date = journal.date
            if queryset.index(journal) != len(queryset)-1:
                if (datetime.date.today() + datetime.timedelta(days=-1)) == datetime.date.today():
                    streak += 1
                else:
                    streak = 0
            print(data)
            if data:
                data_list = json.loads(data)
                # print(type(data_list))
                if data_list:
                    # try:
                    avg_n += 1
                    avg += (data_list["valence"] + data_list["arousal"] + data_list["anger"] + data_list["happiness"] + data_list["sadness"])/5
                    # except Exception as e:
                    #     avg+=0
                    #     avg_n+=0

                    if avg_n > 0:
                        listify.append(avg)
        x_data = [x for x in range(avg_n)]
        y_data = listify
        plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
        
        context = {}
        context["sample_graph"] = plot_div
        print(x_data)
        print(y_data)
        context["avg"] = avg
        # streak = 0
        # for y in range(len(x_data)):
        #     if y == x_data[y]:
        #         streak += 1
        #     elif y != x_data[y]:
        #         streak = 0
        context["streak"] = streak
        if "avg" in context and context["avg"] <= -0.5:
            print("Call therapy!")

        return render(request, self.template_name, context)
# class JournalView(TemplateView):
#     template_name = 'journal/journal.html'

# class TherapistAlert():
