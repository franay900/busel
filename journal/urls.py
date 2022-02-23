from django.urls import path
from .views import *


urlpatterns=[
	path('journal/school',SchoolJournalView.as_view() ,name="JournalView"),
	path('journal/my',MyJournalView.as_view() ,name="MyJournal"),
	path('journal/class',ClassesJournalView.as_view() ,name="ClassJournal"),
	path('journal/delete_topics/<int:load>/<int:period>',DeleteTopics.as_view() ,name="DeleteTopics"),

	path('check_period/<int:load>',check_period ,name="CheckPeriod"),
	path('lesson_topics/<int:load>/<int:period>/',LessonTopics.as_view() ,name="LessonTopics"),
	path('save_mark/',Mark.as_view() ,name="Mark"),
	path('itog/<int:load>/<int:period>',ItogView.as_view() ,name="ItogView"),
	path('get_load/<int:class_pk>/',get_loads ,name="GetLoad"),
	path('return',returnview ,name="returnview"),


	path('timetable/teacher',TeacherTimeatable.as_view() ,name="TimetableTeacher"),
	
	
	path('journal/attendance', AttendanceJournal.as_view(), name='AttendanceJournal'), 
	path('journal/attendance/<int:pk>', AttendanceJournal.as_view(), name='AttendanceJournalPk')
]

