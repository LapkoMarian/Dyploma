import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Journal
from .forms import AddGradeForm


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
        date_list = [start_date - datetime.timedelta(days=x) for x in range(7)]
        students_list = Journal.get_list_students_in_classroom(classroom_id=classroom_id)

        for student in students_list:
            date_rating = []
            for d in date_list:
                date_rating.append(
                    (str(d), Journal.get_rating_date(str(d), student["user_id"], classroom_id))
                )
            student['rating'] = date_rating

        add_grade_form = AddGradeForm()
        return render(
            request=request,
            template_name='journal/journal_teacher.html',
            context={'students_list': students_list, 'add_grade_form': add_grade_form}
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
def add_grade(request, classroom_id: int):
    if request.method == 'POST':
        form = AddGradeForm(request.POST)
        if form.is_valid():
            topik = form.cleaned_data.get('topik')
            rating = form.cleaned_data.get('rating')
            students_list = Journal.get_list_students_in_classroom(classroom_id=classroom_id)
            grade = Journal(rating=rating, created_at=  , classroom_user=  , created_by=request.user, topik=topik, )
            grade.save()
            messages.success(request, f'Оцінка додана!')
        else:
            messages.warning(request, f'Помилка додавання оцінки:(')
    return redirect('journal:view_journal')




# def create_classroom(request):
#     if request.method == 'POST':
#         form = ClassroomCreationForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data.get('name')
#             description = form.cleaned_data.get('description')
#             classroom = Classroom(name=name, description=description, created_by=request.user,
#                                   classroom_code=Classroom.generate_code())
#             classroom.save()
#             topic = Topic(name='General', classroom=classroom)
#             topic.save()
#             classroom_teachers = ClassroomTeachers(classroom=classroom, teacher=request.user)
#             classroom_teachers.save()
#             messages.success(request, f'Classroom {name} created !')
#         else:
#             messages.warning(request, f'Classroom Could not be created :(')
#     return redirect('classroom:home')