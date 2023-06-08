from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required


from .models import Classroom, Topic, ClassroomTeachers
from posts.models import Assignment,SubmittedAssignment,AssignmentFile, Attachment
from .forms import ClassroomCreationForm,JoinClassroomForm, PostForm, AssignmentFileForm, AssignmentCreateForm
from comments.forms import CommentCreateForm


@login_required
def home(request):
    teaching_classes = request.user.classroomteachers_set.all()
    student_classes = request.user.classrooms.all()
    classroom_form = ClassroomCreationForm()
    join_classroom_form = JoinClassroomForm()
    context = {
        'teaching_classes': teaching_classes,
        'student_classes': student_classes,
        'classroom_form': classroom_form,
        'join_classroom_form': join_classroom_form
    }
    return render(request, 'classroom/home.html', context)


@login_required
@permission_required("classroom.add_classroom", raise_exception=True)
def create_classroom(request):
    if request.method == 'POST':
        form = ClassroomCreationForm(request.POST)
        if form.is_valid(): 
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            classroom = Classroom(name=name, description=description, created_by=request.user,
                                  classroom_code=Classroom.generate_code())
            classroom.save()
            topic = Topic(name='General', classroom=classroom)
            topic.save()
            classroom_teachers = ClassroomTeachers(classroom=classroom, teacher=request.user)
            classroom_teachers.save()
            messages.success(request, f'Classroom {name} created !')
        else:
            messages.danger(request, f'Classroom Could not be created :(')
    return redirect('classroom:home')


@login_required
def join_classroom(request):
    if request.method == 'POST':
        form = JoinClassroomForm(request.POST)
        if form.is_valid(): 
            classroom = Classroom.objects.filter(classroom_code = form.cleaned_data.get('code')).first()
            if classroom:
                request.user.classrooms.add(classroom)
                messages.success(request, f'You are added in {classroom.name}')
            else:
                messages.success(request, f'Error adding you to the classroom')
        else:
            messages.success(request, f'Error adding you to the classroom')
    return redirect('classroom:home')


@login_required
def open_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.user in [clt.teacher for clt in classroom.classroomteachers_set.all()] or request.user in classroom.users.all():
        topics = classroom.topic_set.all()
        contents = []
        for topic in topics:
            contents.extend(list(topic.post_set.all()))
            contents.extend(list(topic.assignment_set.all()))

        contents.sort(key=lambda x: x.created_at)

        post_form = PostForm()
        comment_form = CommentCreateForm()

        context = {
            'classroom': classroom,
            'contents': reversed(contents),
            'post_form': post_form,
            'comment_form': comment_form,
        }

        return render(request, 'classroom/classroom.html', context)
    messages.error(request, f'Ви не є учасником цього класу!')
    return redirect('classroom:home')


@login_required
def leave_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.user in classroom.users.all():
        request.user.classrooms.remove(classroom)
        messages.success(request, f'Ви покинули клас!')
    else:
        messages.error(request, f'Ви не є учасником цього класу!')

    return redirect('classroom:home')


@login_required
@permission_required("classroom.delete_classroom", raise_exception=True)
def delete_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.user in [clt.teacher for clt in classroom.classroomteachers_set.all()]:
        classroom.delete()
        messages.success(request, f'Клас успішно видалено.')
    else:
        messages.error(request, f'Ви не можете видалити клас! Це може зробити тільки вчитель!')
    return redirect('classroom:home')


@login_required
def members(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    context = {
        'teachers': classroom.classroomteachers_set.all(),
        'students': classroom.users.all(),
    }
    return render(request, 'classroom/members.html', context)


@login_required
@permission_required("posts.add_assignment", raise_exception=True)
def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentCreateForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            topic = get_object_or_404(Topic, pk=int(form.cleaned_data['topics']))
            assignment = Assignment(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                created_by = request.user,
                topic = topic,
                due_date = form.cleaned_data['due_date']
            )
            assignment.save()
            files = request.FILES.getlist('file_field')
            for f in files:
                Attachment.objects.create(assignment = assignment,files=f)
            return redirect('classroom:open_classroom', topic.classroom.pk)

    else:
        form = AssignmentCreateForm(request.user)
    context = {'form': form}
    return render(request, 'classroom/assignment_create.html', context)


@login_required
def assignment_submit(request, pk):
    if request.method=='POST':
        assignment = get_object_or_404(Assignment,pk=pk)
        submitted_assignment = assignment.submittedassignment_set.filter(user = request.user).first()
        if not submitted_assignment:
            submitted_assignment = SubmittedAssignment.objects.create(assignment = assignment, user = request.user)
        files = request.FILES.getlist('file_field')
        for f in files:
            AssignmentFile.objects.create(submitted_assignment = submitted_assignment,files=f)
    
    form = AssignmentFileForm()
    assignment = get_object_or_404(Assignment, pk=pk)
    submit_assignment = assignment.submittedassignment_set.filter(user=request.user)
    classroom_teachers = list(map(lambda teaches: teaches.teacher, assignment.topic.classroom.classroomteachers_set.all()))
    is_teacher = request.user in classroom_teachers
    if submit_assignment:
        submit_assignment = submit_assignment.first()
        assignment_files = submit_assignment.assignmentfile_set.all()
    else:
        assignment_files = None

    context = {
        'assignment': assignment,
        'attachments': assignment.attachment_set.all(),
        'submitted_assignment': submit_assignment,
        'assignment_files': assignment_files,
        'form': form,
        'is_teacher': is_teacher,
    }
    return render(request, 'classroom/assignment_submit.html', context)


@login_required
def turnin(request,pk):
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment,pk=pk)
        submitted_assignment = assignment.submittedassignment_set.filter(user = request.user).first()
        if not submitted_assignment:
            submitted_assignment = SubmittedAssignment.objects.create(assignment = assignment, user = request.user)
        submitted_assignment.turned_in = True 
        submitted_assignment.save()
        
    return redirect('classroom:assignment_submit', pk)


@login_required
def unsubmit(request,pk):
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment,pk=pk)
        submitted_assignment = assignment.submittedassignment_set.filter(user = request.user).first()
        submitted_assignment.turned_in = False  
        submitted_assignment.save()
        
    return redirect('classroom:assignment_submit', pk)


@login_required
def unsubmit_file(request, pk):
    if request.method == 'POST':
        assignment_file = get_object_or_404(AssignmentFile, pk=pk)
        assignment_pk = assignment_file.submitted_assignment.assignment.pk
        if assignment_file.submitted_assignment.user == request.user:
            if assignment_file.submitted_assignment.turned_in:
                submitted_assignment = assignment_file.submitted_assignment
                submitted_assignment.turned_in = False  
                submitted_assignment.save()
            assignment_file.delete()
        return redirect('classroom:assignment_submit', assignment_pk)


@login_required
def todo(request):
    classrooms = request.user.classroom_set.all()
    topics = []
    for classroom in classrooms:
        topics.extend(list(classroom.topic_set.all()))
    assignments = []
    for topic in topics:
        assignments.extend(list(topic.assignment_set.all()))
    filtered_assignment = []
    for assignment in assignments:
        if not assignment.is_turnedin(request.user):
            filtered_assignment.append(assignment)
    context = {'assignments': filtered_assignment}
    
    return render(request, 'classroom/todo.html', context)


@login_required
def toreview(request):
    classrooms = request.user.classroomteachers_set.all()
    classrooms = list(map(lambda x: x.classroom, classrooms))
    topics = []
    for classroom in classrooms:
        topics.extend(classroom.topic_set.all())
    assignments = []
    for topic in topics:
        assignments.extend(topic.assignment_set.all())
    context = {'assignments': reversed(assignments)}
    return render(request, 'classroom/toreview.html', context)


@login_required
def classwork(request, pk):
    classroom = get_object_or_404(Classroom,pk=pk)
    assignments = []
    for topic in classroom.topic_set.all():
        assignments.extend(list(topic.assignment_set.all()))
    
    context = {'assignments':assignments}
    return render(request, 'classroom/classwork.html', context)


@login_required
def student_work(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    context = {'assignment': assignment}
    return render(request, 'classroom/student_work.html', context)



