from django.urls import path

import journal.views as views

urlpatterns = [
<<<<<<< Updated upstream
    path('journal-add', views.JournalAddView.as_view(), name='journal-add'),
    path('journal-detail/<int:pk>/', views.JournalDetailView.as_view(), name='journal-detail'),
    # path('journal-add', views.JournalAddView.as_view()),
    # path('journal-view/<int:pk>/', views.JournalDetailView.as_view())

=======
    path('', views.JournalAddView.as_view(), name='journal-add'),
    path('journal-detail', views.JournalDetailView.as_view(), name='journal-detail'),
>>>>>>> Stashed changes
]