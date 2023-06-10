from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from .models import Assignment, Post,Resource
from classroom.models import Classroom,Topic
from classroom.forms import PostForm


@login_required
@permission_required("posts.add_post", raise_exception=True)
def create_post(request, pk):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            classroom = get_object_or_404(Classroom,pk = pk)
            topic = classroom.topic_set.first()
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            files = request.FILES.getlist('file_field')
            post = Post.objects.create(title=title,description=description,created_by=request.user, topic = topic)
            for f in files:
                Resource.objects.create(post = post,files=f)
            
            messages.success(request, f'Створено пост {title}')
        else:
            messages.danger(request, f'Не створено пост')
    
    return redirect('classroom:open_classroom', pk)


@login_required
@permission_required("posts.change_post", raise_exception=True)
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post.topic = classroom.topic_set.first()
            post.title = form.cleaned_data.get('title')
            post.description = form.cleaned_data.get('description')
            post.save()
            files = request.FILES.getlist('file_field')
            for f in files:
                Resource.objects.update(post=post, files=f)

            messages.success(request, f'Відредаговано пост {post.title}')
        else:
            messages.danger(request, f'Не відредаговано пост')

    return redirect('classroom:open_classroom', classroom.pk)


@login_required
@permission_required("classroom.delete_post", raise_exception=True)
def delete_post(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    post = get_object_or_404(PostForm, pk=pk)
    if request.user in [clt.teacher for clt in classroom.classroomteachers_set.all()]:
        post.delete()
        messages.success(request, f'Пост успішно видалено.')
    else:
        messages.error(request, f'Ви не можете видалити пост! Це може зробити тільки вчитель!')
    return redirect('classroom:open_classroom', classroom.pk)