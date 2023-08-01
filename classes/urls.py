from django.urls import path
from .views import *


urlpatterns=[
	path('class_view/',ClassView.as_view() ,name="Class"),
	path('class_edit/<int:pk>/',class_edit_view ,name="ClassEdit"),
	path('delete_class/',DeleteClassView.as_view() ,name="ClassDelete"),

	path('subgroup/',SubgroupView.as_view() ,name="SubgroupView"),
	path('subgroup/<int:pk>/',SubgroupView.as_view() ,name="SubgroupViewPk"),

	path('сurriculum/',СurriculumView.as_view() ,name="Curriculum"),
	path('сurriculum_edit/<int:pk>',СurriculumUpdateView.as_view() ,name="CurriculumEdit"),
	path('add_сurriculum/',СurriculumCreateView.as_view() ,name="AddCurriculum"),
	path('сurriculum_delete/<int:pk>',DeleteCurriculum.as_view() ,name="DeleteCurriculum"),

	path('load/',LoadView.as_view() ,name="Load"),
	path('load/<int:pk>/',LoadView.as_view() ,name="LoadPk"),\

	path('student/add/',AddStudent.as_view() ,name="StudentAdd"),
	path('student/import/',ImportStudent.as_view() ,name="StudentImport"),
	path('student/edit/<int:student_pk>',StudentEditView.as_view() ,name="StudentEdit"),
	path('student/list/',StudentListView.as_view() ,name="StudentList"),
	path('student/list/<str:delete_code>/',StudentListView.as_view() ,name="StudentList"),
	path('student/cancel_import/<str:delete_code>/',CancelImport.as_view() ,name="CancelImport"),
	path('student/export',ExportStudent.as_view() ,name="StudentExport"),

	path('delete_student/',Deduction.as_view() ,name="DeleteStudent"),
	path('get_students/<int:class_pk>/',ReturnStudents.as_view(), name="GetStudent"),

	path('timetable/classes/',Timetable.as_view() ,name="TimetableClasses"),
	path('timetable/templates/<int:pk>/',TimetableTemplatesView.as_view() ,name="TimetableTemplates"),
	path('timetable/add_template/',AddTimetableTemplate.as_view() ,name="AddTimetableTemplate"),
	path('timetable/create_template/',CreateTimetableTemplate.as_view() ,name="CreateTimetableTemplate"),
	path('timetable/update_template/<int:pk>/',UpdateTimetableTemplate.as_view() ,name="UpdateTimetableTemplate"),
	path('timetable/weeks/<int:pk>/',TimetableWeek.as_view() ,name="TimetableWeek"),
	path('timetable/weeks/<int:period>/<int:pk>/',TimetableWeek.as_view() ,name="TimetableWeekPk"),
	
	path('edit_lesson/<int:class_pk>/',EditLessons.as_view() ,name="EditLesson"),
	path('delete_lessons/<int:class_pk>/',DeleteLessons.as_view() ,name="DeleteLessons"),


	
]

