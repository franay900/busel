from django.contrib import admin
from .models import UserNet,FileTemplates
from django.contrib.auth.models import Permission



admin.site.register(FileTemplates)
admin.site.register(Permission)



@admin.register(UserNet)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "middle_name", "birth_day", "institution")
    fields = ("last_name", "first_name", "middle_name", "birth_day", "gender","code","institution")