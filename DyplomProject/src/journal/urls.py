from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.view_list_group, name='view_list'),
]
