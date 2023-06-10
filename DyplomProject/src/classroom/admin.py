from django.contrib import admin
from . import models
from django import forms

admin.site.register(models.Classroom)
admin.site.register(models.ClassroomUsers)
admin.site.register(models.Topic)
