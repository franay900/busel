from django.urls import path
from .views import *


urlpatterns=[
	path('',JournalView.as_view() ,name="JournalView"),
	path('check_period/<int:load>',check_period ,name="CheckPeriod"),
	path('lesson_topics/<int:load>/<int:period>/',LessonTopics.as_view() ,name="LessonTopics"),
	path('save_mark/',Mark.as_view() ,name="Mark"),
	path('itog/<int:load>/<int:period>',ItogView.as_view() ,name="ItogView"),
	path('get_load/<int:class_pk>/',get_loads ,name="GetLoad"),
	
]

