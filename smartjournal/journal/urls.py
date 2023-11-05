from django.urls import path

import journal.views as views

urlpatterns = [
    path('', views.JournalAddView.as_view(), name='journal-add'),
    path('journal-detail', views.JournalDetailView.as_view(), name='journal-detail'),
]