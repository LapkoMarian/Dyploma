from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Lesson, Weekday, Schedule, Call, Form
from users.models import StudentsForm


@login_required
def view_schedule(request):
    forms = []
    schedules = Schedule.objects.all()
    students_form = get_object_or_404(StudentsForm, user=request.user)
    if request.user.profile.is_student:
        schedules = Schedule.objects.filter(class_name=students_form.form)
        forms = Form.objects.filter(class_name=students_form.form)
        print(schedules)
    else:
        print(schedules)
        schedules = Schedule.objects.filter(teacher=request.user)
    weekdays = Weekday.objects.all()
    calls = Call.objects.all()

    context = {
        'schedules': schedules,
        'weekdays': weekdays,
        'forms': forms,
        'calls': calls,
    }

    return render(request, 'schedule/schedule.html', context)


def view_calls(request):
    calls = Call.objects.all()
    context = {
        'calls': calls,
    }

    return render(request, 'schedule/calls.html', context)
