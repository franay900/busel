from django.urls import path
from .views import *



urlpatterns=[
	
	path('home/',Home.as_view() ,name="HomeDiary"),
	path('grade/',GradeReport.as_view() ,name="Grade"),

	
]