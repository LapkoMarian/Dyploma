from django.contrib import admin
from django.contrib.auth.models import User
from . import models
from django import forms


class LessonAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            # Отримати queryset з користувачами, які належать до групи з ідентифікатором 1
            kwargs["queryset"] = User.objects.filter(groups__id=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(models.Journal, LessonAdmin)

