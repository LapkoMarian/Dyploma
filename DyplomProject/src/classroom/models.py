from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random


# members are not teachers
class Classroom(models.Model):
    name = models.CharField(max_length=200)
    classroom_code = models.CharField(max_length=20, blank=True)
    description = models.TextField(max_length=300)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    users = models.ManyToManyField(User, related_name='users')

    @staticmethod
    def generate_code(length=6):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(length))

    # @staticmethod
    # def members_classroom():
    #     students = User.objects.filter(groups__name='student')
    #     teachers = User.objects.filter(groups__name='teacher')
    #     return students, teachers

    def __str__(self):
        return f'{self.name}'


class ClassroomTeachers(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher.username} -> {self.classroom.name}'


class Topic(models.Model):
    name = models.CharField(max_length=200)
    classroom = models.ForeignKey(Classroom,on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.classroom.name} -> {self.name}'







