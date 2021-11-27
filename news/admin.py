from django.contrib import admin
from .models import News,Category
from user_account.models import UserNet
admin.site.register(News)
admin.site.register(Category)
