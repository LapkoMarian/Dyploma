from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta


class Call(models.Model):
    lesson_number = models.IntegerField(default=0)
    starting_lesson = models.CharField(max_length=5)
    ending_lesson = models.CharField(max_length=5)
    pause = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.lesson_number}'


class Lesson(models.Model):
    name_lesson = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name_lesson}'


class Weekday(models.Model):
    name_day = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name_day}'


class Form(models.Model):
    class_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.class_name}'


class ScheduleReplacement(models.Model):
    name_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name_lesson} -> {self.teacher}'


class Schedule(models.Model):
    class_name = models.ForeignKey(Form, on_delete=models.CASCADE)
    days = models.ForeignKey(Weekday, on_delete=models.CASCADE)
    number_lesson = models.ForeignKey(Call, on_delete=models.CASCADE)
    name_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    replacement = models.ForeignKey(ScheduleReplacement, on_delete=models.CASCADE, default=None, null=True, blank=True)
    replacement_range = models.DurationField(default=timedelta(days=2))

    def is_actual_replacement(self):
        if date.today() <= self.replacement_range:
            self.replacement.delete()
            return False
        else:
            return True

    def __str__(self):
        return f'{self.class_name} -> {self.days} -> {self.number_lesson} урок -> {self.name_lesson} -> ' \
               f'{self.teacher.last_name} {self.teacher.first_name}'

