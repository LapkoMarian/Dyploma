from django.urls import path, include
from . import views

app_name = 'comments'

urlpatterns = [
    path('create/<int:post_pk>/', views.create_post_comment, name='create_post_comment'),
    path('assignment_comment/create/<int:assignment_pk>/', views.create_assignment_comment, name='create_assignment_comment'),
]