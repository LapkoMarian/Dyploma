from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.view_journal_list, name='view_list'),
    path('<int:classroom_id>', views.view_journal, name='view_teacher_journal'),
    path('add_grade/', views.add_grade, name='add_grade'),
]
