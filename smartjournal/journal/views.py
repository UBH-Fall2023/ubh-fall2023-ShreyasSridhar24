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
# import speech_recognition as sr

from plotly.offline import plot
from plotly.graph_objs import Scatter, Layout, Pie, Figure

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

# class JournalAddView(LoginRequiredMixin, FormView):

# class GetAudio(FormView):
#     model = Journal
#     def get(self):

        
#         # files = form_data.get('files')

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
        files = form_data.get('files')
        audio = form_data.get("audio_file")
        # files = form_data.get('files')

        if(image):
            image_ = Image.open(image)
            text = pytesseract.image_to_string(image_, lang="eng")
            message = str(text)
        elif(files):
            message = ""
            with open(files,"rb") as f:
                for m in f.readlines():
                    message+=m
        # elif(audio):
        #     print("omg audion")
        #     r = sr.Recognizer()
        #     with sr.AudioFile(audio) as source:
                
        #         audio_text = r.listen(source)
                
        #     # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        #         # try:
                    
        #         # using google speech recognition
        #         text = r.recognize_google(audio_text)
        #         print('Converting audio transcripts into text ...')
        #         print(text)
        #         message = text
                    
                # except:
                #     print('Sorry.. run again...')



        # image = form_data.get('image')  
        # print(type(image))          
        
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
            {"role": "system", "content": "Give me a dictionary in JSON of the valence-arousal,anger,happiness,sadness scores of the following sentence on a scale of -1 to 1. \""+message+"\""},
            # {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
        )
        data = completion.choices[0].message["content"]


        journal_entry = Journal.objects.create(title = fernet.encrypt(title.encode()), message = fernet.encrypt(message.encode()), date = date, is_private = is_private, image = image, files = files, data = data)
        reader = easyocr.Reader(['en'])
        image_words = reader.readtext(image.read(), detail=0)
        journal_entry = Journal.objects.create(title = title, message = fernet.encrypt(message.encode()), date = date, is_private = is_private, image = image, file = file)
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
        print(type(queryset))
        queryset = list(queryset)
        valence = []
        arousal = []
        anger = []
        happiness = []
        sadness = []
        for journal in queryset:
            data = journal.data
            date = journal.date
            # if 
            if queryset.index(journal) != 0:
                if (queryset[queryset.index(journal)-1].date + datetime.timedelta(days=+1)) == date:
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
                    happiness.append(data_list["happiness"])
                    sadness.append(data_list["sadness"])
                    anger.append(data_list["anger"])
                    arousal.append(data_list["arousal"])
                    valence.append(data_list["valence"])
                    avg += (data_list["valence"] + data_list["arousal"] + data_list["anger"] + data_list["happiness"] + data_list["sadness"])/5
                    # except Exception as e:
                    #     avg+=0
                    #     avg_n+=0

                    if avg_n > 0:
                        listify.append(avg)
        x_data = [x for x in range(avg_n)]
        y_data = listify
        y_data_ = len(valence)
        d1 = Scatter(y=valence, x=y_data, mode='lines', name='Valence')
        d2 = Scatter(y=happiness, x=y_data, mode='lines', name='Happiness')
        d3 = Scatter(y=sadness, x=y_data, mode='lines', name='Sadness')
        d4 = Scatter(y=anger, x=y_data, mode='lines', name='Anger')
        d5 = Scatter(y=arousal, x=y_data, mode='lines', name='Arousal')
        d6 = Scatter(y=x_data, x=y_data, mode='lines', name='Average')
        data_ = [d1,d2,d3,d4,d5,d6]
        layout_ = Layout(title='Multiple Lines Scatter Plot',
        xaxis=dict(title='X-Axis'),
        yaxis=dict(title='Y-Axis')
    )
        fig = Figure(data=data_, layout=layout_)
        plot_div = fig.to_html(full_html=False)
        # context["sample_graph"] = plot_div

        d1 = Pie(values=[sum(valence),sum(happiness),sum(sadness),sum(anger),sum(arousal),sum(x_data)],labels=['Valence','Happiness','Sadness','Anger','Arousal','Average'])
        # d2 = Pie(y=sum(happiness), label='Happiness')
        # d3 = Pie(y=sum(sadness), label='Sadness')
        # d4 = Pie(y=sum(anger), label='Anger')
        # d5 = Pie(y=sum(arousal), label='Arousal')
        # d6 = Pie(y=sum(x_data), label='Average')
        data__ = d1
        layout__ = Layout(title='Pie Plot of Emotions since the first entry',
        
    )
        fig = Figure(data=data__, layout=layout__)
        plot_div_ = fig.to_html(full_html=False)
        context["sample_graph"] = plot_div
        context["pie_graph"] = plot_div_
        # plot([Scatter(x=valence, y=y_data,
        #                 mode='lines', name='valence',
        #                 opacity=0.8, marker_color='orange')],
        #        output_type='div')
        # plot([Scatter(x=arousal, y=y_data,
        #                 mode='lines', name='arousal',
        #                 opacity=0.8, marker_color='blue')],
        #        output_type='div')
        # plot([Scatter(x=happiness, y=y_data,
        #                 mode='lines', name='happiness',
        #                 opacity=0.8, marker_color='green')],
        #        output_type='div')
        # plot([Scatter(x=sadness, y=y_data,
        #                 mode='lines', name='sadness',
        #                 opacity=0.8, marker_color='red')],
            #    output_type='div')
        # plot([Scatter(x=x_data, y=y_data,
        #                 mode='lines', name='test',
        #                 opacity=0.8, marker_color='green')],
        #        output_type='div')
        # plot([Scatter(x=x_data, y=y_data,
        #                 mode='lines', name='test',
        #                 opacity=0.8, marker_color='green')],
        #        output_type='div')
        
        # context = {}
        # context["sample_graph"] = plot.show()
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
