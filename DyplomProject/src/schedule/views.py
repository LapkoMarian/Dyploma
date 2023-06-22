from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Lesson, Weekday, Schedule, Call, Form
from users.models import StudentsForm


@login_required
def view_schedule(request):
    forms = []
    if request.user.profile.is_student():
        students_form = StudentsForm.objects.get(user=request.user)
        schedules = Schedule.objects.filter(class_name=students_form.form).all()
        forms = Form.objects.filter(class_name=students_form.form).all()
        replacements = Schedule.objects.filter(class_name=students_form.form, replacement__isnull=False)
    elif request.user.profile.is_teacher():
        schedules = Schedule.objects.filter(teacher=request.user).all()
        replacements = Schedule.objects.filter(teacher=request.user, replacement__isnull=False)
    weekdays = Weekday.objects.all()
    calls = Call.objects.all()

    context = {
        'schedules': schedules,
        'replacements': replacements,
        'weekdays': weekdays,
        'forms': forms,
        'calls': calls,
    }

    return render(request, 'schedule/schedule.html', context)


def view_calls(request):
    calls = Call.objects.all()
    return render(request, 'schedule/calls.html', {'calls': calls})
