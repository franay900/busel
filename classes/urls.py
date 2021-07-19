from django.urls import path
from .views import *


urlpatterns=[
	path('class_view/',ClassView.as_view() ,name="Class"),
	path('class_edit/<int:pk>/',class_edit_view ,name="ClassEdit"),
	path('сurriculum/',СurriculumView.as_view() ,name="Curriculum"),
	path('add_сurriculum/',СurriculumCreateView.as_view() ,name="AddCurriculum"),
	path('load/',LoadView.as_view() ,name="Load"),
	path('load/<int:pk>/',LoadView.as_view() ,name="LoadPk"),
	path('timetable/classes/',Timetable.as_view() ,name="TimetableClasses"),
	path('timetable/templates/<int:pk>/',TimetableTemplatesView.as_view() ,name="TimetableTemplates"),
	path('timetable/add_template/',AddTimetableTemplate.as_view() ,name="AddTimetableTemplate"),
	path('timetable/create_template/',CreateTimetableTemplate.as_view() ,name="CreateTimetableTemplate"),
	path('timetable/update_template/<int:pk>/',UpdateTimetableTemplate.as_view() ,name="UpdateTimetableTemplate"),
	path('timetable/weeks/<int:pk>/',TimetableWeek.as_view() ,name="TimetableWeek"),
	path('timetable/weeks/<int:period>/<int:pk>/',TimetableWeek.as_view() ,name="TimetableWeekPk"),
	path('student/list/',StudentListView.as_view() ,name="StudentList"),
	path('student/add/',AddStudent.as_view() ,name="StudentAdd"),
	path('student/import/',ImportStudent.as_view() ,name="StudentImport"),
	
	
]

