from django.urls import path
from .views import *


urlpatterns=[
	path('',ReportsView.as_view() ,name="ReportsView"),
	path('journal',ReportJournal.as_view() ,name="ReportsJournal"),

	path('performance',ReportPerformance.as_view() ,name="ReportPerformance"),
	path('performance/<int:class_pk>',ReportPerformance.as_view() ,name="ReportPerformancePk"),

	path('get_periods/<int:class_pk>',get_period ,name="GetPeriods"),
]

