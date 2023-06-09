from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random


class Classroom(models.Model):
    name = models.CharField(max_length=200, unique=True)
    classroom_code = models.CharField(max_length=20, blank=True)
    description = models.TextField(max_length=300)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    users = models.ManyToManyField(User, related_name='classrooms', through='ClassroomUsers')

    @staticmethod
    def generate_code(length=6):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(length))

    def __str__(self):
        return f'{self.name}'


class ClassroomTeachers(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher.username} -> {self.classroom.name}'


class ClassroomUsers(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} -> {self.classroom.name}'

    class Meta:
        db_table = "classroom_classroom_users"
        unique_together = ('classroom', 'user')


class Topic(models.Model):
    name = models.CharField(max_length=200)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.classroom.name} -> {self.name}'
