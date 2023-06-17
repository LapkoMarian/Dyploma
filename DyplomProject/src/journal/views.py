import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Journal


# Create your views here.


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
        date_list = [start_date - datetime.timedelta(days=x) for x in range(5)]
        students_list = Journal.get_list_students_in_classroom(classroom_id=classroom_id)

        for student in students_list:
            date_rating = []
            print(student)
            for d in date_list:
                date_rating.append(
                    (str(d), Journal.get_rating_date(str(d), student["user_id"], classroom_id))
                )
            student['rating'] = date_rating

        return render(
            request=request,
            template_name='journal/journal_teacher.html',
            context={'students_list': students_list}
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
