# complaints/urls.py

from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('create/', views.create_complaint, name='create_complaint'),
    path('new/',  views.create_complaint, name='create_complaint'),
    path('mine/', views.list_complaints,  name='list_complaints'),
]
