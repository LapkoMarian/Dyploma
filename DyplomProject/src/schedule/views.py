from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Lesson, Weekday, Schedule, Call, Clas


def view_schedule(requests):
    schedules = Schedule.objects.all()
    lessons = Lesson.objects.all()
    weekdays = Weekday.objects.all()
    calls = Call.objects.all()
    classes = Clas.objects.all()
    context = {
        'schedules': schedules,
        'lessons': lessons,
        'weekdays': weekdays,
        'calls': calls,
        'classes': classes,
    }
    return render(requests, 'schedule/schedule.html', context)