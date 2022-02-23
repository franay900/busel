from django.contrib import admin
from .models import *
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from user_account.models import UserNet

admin.site.register(Institutions)
admin.site.register(Year)
admin.site.register(TypeInstitutions)
admin.site.register(BellProfile)
admin.site.register(BellTimetable)
admin.site.register(Subject)
admin.site.register(SystemMarks)
admin.site.register(KindInstitutions)


admin.site.site_header = 'Админ-панель ПК "Бусел"'
