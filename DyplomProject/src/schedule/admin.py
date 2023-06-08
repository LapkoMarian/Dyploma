from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat

from . import models

admin.site.register(models.Weekday)
admin.site.register(models.Call)
admin.site.register(models.Lesson)
admin.site.register(models.Form)


class LessonAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            # Отримати queryset з користувачами, які належать до групи з ідентифікатором 1
            kwargs["queryset"] = User.objects.filter(groups__id=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(models.Schedule, LessonAdmin)


