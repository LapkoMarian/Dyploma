from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from classroom.models import ClassroomUsers


class Rating(models.IntegerChoices):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    eleven = 11
    twelve = 12


class Journal(models.Model):
    rating = models.IntegerField(choices=Rating.choices)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    classroom_user = models.ForeignKey(ClassroomUsers, on_delete=models.CASCADE)
