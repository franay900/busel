from django.contrib import admin
from .models import LessonType, Lessons


admin.site.register(LessonType)
admin.site.register(Lessons)