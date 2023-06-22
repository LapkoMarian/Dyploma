import datetime
import locale

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from classroom.models import Classroom
from .models import Journal
from .forms import AddGradeForm


@login_required
def view_journal_list(request):
    if request.user.profile.is_teacher():
        list_classroom = Journal.get_list_teacher_classroom(teacher_id=request.user.id)
    else:
        list_classroom = Journal.get_list_student_classroom(student_id=request.user.id)

    return render(
        request=request,
        template_name='journal/journal_list.html',
        context={'list_classroom': list_classroom}
    )


def view_journal(request, classroom_id: int):
    if request.user.profile.is_teacher():
        start_date = str(request.GET.get("start_date", datetime.date.today()))
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        date_list = []

        for x in range(7):
            date = start_date + datetime.timedelta(days=x)
            if date.weekday() < 5:
                date_list.append(date)

        students_list = Journal.get_list_students_in_classroom(classroom_id=classroom_id)

        for student in students_list:
            date_rating = []
            for d in date_list:
                date_rating.append(
                    (str(d), Journal.get_rating_date(str(d), student["user_id"], classroom_id))
                )
            student['rating'] = date_rating
        add_grade_form = AddGradeForm()
        classroom = get_object_or_404(Classroom, id=classroom_id)
        class_name = classroom.name
        return render(
            request=request,
            template_name='journal/journal_teacher.html',
            context={'students_list': students_list, 'add_grade_form': add_grade_form, 'class_name': class_name}
        )
    else:
        rating = Journal.get_student_rating(
            student_id=request.user.id,
            classroom_id=classroom_id
        )

        return render(
            request=request,
            template_name='journal/journal_student_rating.html',
            context={'rating': rating}
        )


@login_required
def add_grade(request):
    if request.method == 'POST':
        form = AddGradeForm(request.POST)
        if form.is_valid():
            topik = form.cleaned_data.get('topik')
            rating = form.cleaned_data.get('rating')
            created_at = form.cleaned_data.get('created_at')
            classroom_user = form.cleaned_data.get('classroom_user')

            Journal(
                rating=rating,
                created_at=created_at,
                classroom_user=classroom_user,
                created_by=request.user, topik=topik
            ).save()

            messages.success(request, f'Оцінка додана!')

        else:
            messages.warning(request, f'Помилка додавання оцінки:(')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



