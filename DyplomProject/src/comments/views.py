from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from .forms import CommentCreateForm
from .models import PostComment, AssignmentComment
from posts.models import Post, Assignment


@login_required
def create_post_comment(request, post_pk):
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=post_pk)
            comment = PostComment(
                user=request.user, 
                comment_text=form.cleaned_data.get('comment_text'),
                post=post
            )
            comment.save()
            return redirect('classroom:open_classroom', post.topic.classroom.pk)


@login_required
def create_assignment_comment(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = AssignmentComment(
                user=request.user,
                comment_text=form.cleaned_data.get('comment_text'),
                assignment=assignment
            )
            comment.save()
            return redirect('classroom:assignment_submit', assignment.pk)
