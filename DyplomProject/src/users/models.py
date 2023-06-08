from django.db import models
from django.contrib.auth.models import User
from schedule.models import Form
from PIL import Image


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='users/profile_pics/default.jpg', upload_to='users/profile_pics/')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def is_teacher(self):
        if self.user.groups.filter(id=1):
            return True
        else:
            return False

    def is_student(self):
        if self.user.groups.filter(id=2):
            return True
        else:
            return False


class StudentsForm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    form = models.OneToOneField(Form, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.form.class_name}'

