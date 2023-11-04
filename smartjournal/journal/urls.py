from django.urls import path

import journal.views as views

urlpatterns = [
    path('journal-add', views.JournalAddView.as_view())
]