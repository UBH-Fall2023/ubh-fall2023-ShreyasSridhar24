from django.urls import path
from django.views.generic import TemplateView
import journal.views as views

urlpatterns = [
    path('home', TemplateView.as_view(template_name='homepage.html')),
    path('', views.JournalAddView.as_view(), name='journal-add'),
    path('journal-detail/<int:pk>', views.JournalDetailView.as_view(), name='journal-detail'),
    path('journal-dashboard', views.JournalOverview.as_view(), name='journal-dashboard'),
]
