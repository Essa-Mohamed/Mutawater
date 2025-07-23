from django.urls import path
from . import views

app_name = 'exams'
urlpatterns = [
    path('select-scope/', views.select_scope, name='select_scope'),
    path('select-type/',  views.select_type,  name='select_type'),
    path('start/',        views.show_question, name='show_question'),  # if you use `start/` or merge into show_question
    path('question/<int:session_id>/<int:q_no>/', views.show_question, name='show_question'),
    path('finish/<int:session_id>/', views.finish_test, name='finish_test'),
]
