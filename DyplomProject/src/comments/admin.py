from django.contrib import admin
from .models import PostComment, AssignmentComment

admin.site.register(PostComment)
admin.site.register(AssignmentComment)

