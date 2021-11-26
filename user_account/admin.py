from django.contrib import admin
from .models import UserNet,FileTemplates
from django.contrib.auth.models import Permission



admin.site.register(UserNet)
admin.site.register(FileTemplates)
admin.site.register(Permission)
