from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Journal


# Create your views here.


@login_required
def view_list_group(request):
    if request.user.profile.is_teacher:
        pass
    else:
        pass

    rating = Journal.get_rating(student_id= request.user.id)
    return render(request, 'journal/group_list.html', context={'rating': rating})
