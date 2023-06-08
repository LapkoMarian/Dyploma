from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.view_schedule, name='schedule'),
    path('calls/', views.view_calls, name='calls'),
]