from django.contrib import admin
from .models import *
admin.site.register(Classes)
admin.site.register(СurriculumSubject)




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_pk', 'date_of_enrollment')