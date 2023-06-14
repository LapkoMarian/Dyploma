from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.datastructures import MultiValueDict

from .models import Assignment, Post,Resource
from classroom.models import Classroom,Topic
from classroom.forms import PostForm


@login_required
@permission_required("posts.add_post", raise_exception=True)
def create_post(request, pk):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            classroom = get_object_or_404(Classroom, pk=pk)
            topic = classroom.topic_set.first()
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            files = request.FILES.getlist('file_field')
            post = Post.objects.create(title=title,description=description,created_by=request.user, topic = topic)
            for f in files:
                Resource.objects.create(post=post,files=f)
            
            messages.success(request, f'Створено пост {title}')
        else:
            messages.warning(request, f'Не створено пост')
    
    return redirect('classroom:open_classroom', pk)


@login_required
@permission_required("posts.change_post", raise_exception=True)
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.created_by:
        if request.method == 'POST':
            form = PostForm(data=request.POST, files=request.FILES,
                            initial={'title': post.title,
                                     'description': post.description})

            if form.is_valid():
                post.title = form.cleaned_data.get('title')
                post.description = form.cleaned_data.get('description')
                post.save()
                files = request.FILES.getlist('file_field')
                if form.cleaned_data.get('owerride_files'):
                    for resource in post.resources:
                        resource.delete()
                for f in files:
                    Resource.objects.create(post=post, files=f)

                messages.success(request, f'Відредаговано пост {post.title}')
                return redirect('classroom:open_classroom', post.topic.classroom.pk)
            else:
                messages.error(request, f'Не відредаговано пост')
        else:
            form = PostForm(initial={'title': post.title, 'description': post.description})
        context = {'form': form, 'post': post}
        return render(request, 'classroom/edit_post.html', context)
    else:
        messages.warning(request, f'Ви не можете редагувати цей пост! Це може зробити тільки автор цього поста!')
    return redirect('classroom:open_classroom', post.topic.classroom.pk)


@login_required
@permission_required("posts.delete_post", raise_exception=True)
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.created_by:
        post.delete()
        messages.success(request, f'Пост успішно видалено.')
    else:
        messages.warning(request, f'Ви не можете видалити цей пост! Це може зробити тільки автор цього поста!')
    return redirect('classroom:open_classroom', post.topic.classroom.pk)
