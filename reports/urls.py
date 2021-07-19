from django.urls import path
from .views import *


urlpatterns=[
	path('',ReportsView.as_view() ,name="ReportsView"),
	path('journal',ReportJournal.as_view() ,name="ReportsJournal"),

]

