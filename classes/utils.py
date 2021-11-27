from classes.models import Classes, BellTimetable
from journal.models import Lessons
from .models import СurriculumSubject, Load
from modules.weeks import get_all_weeks, get_dates
from institutions.models import Periods
from user_account.models import UserNet
from datetime import datetime


class TimetableSettigns():
    def get_class(self):
        try:
            if 'pk' in self.kwargs:
                class_info=Classes.objects.get(pk=self.kwargs['pk'])
            else:
                class_info=Classes.objects.filter(institution=self.request.user.institution).first()
        except Classes.DoesNotExist:
            class_info=None

        return class_info 
    def get_info(self):
        info_class=self.get_class()
        if info_class!=None:
            subjects=СurriculumSubject.objects.filter(class_number=info_class.class_number,profile=info_class.сurriculum)
        else: subjects=None
        return subjects
    def get_date(self):
        if self.request.GET.get("date"):
            return self.request.GET.get("date")
        else:
            return datetime.today().strftime("%Y-%m-%d")

    def get_period(self):
        if 'period' in self.kwargs:
            period= Periods.objects.get(pk=self.kwargs['period'])
        else:
            period= Periods.objects.filter(profile=self.get_class().period_profile).first()
        return period
    def get_weeks(self):
        d_start = str(self.get_period().start)
        d_end = str(self.get_period().end)
        weeks = [*get_all_weeks(d_start, d_end)]
        return weeks

    def get_lessons(self):
        try:
            return Lessons.objects.filter(date=self.get_date(),class_pk=self.get_class()).order_by("number")
        except Lessons.DoesNotExist:
            return None

    def get_loads(self):
        return Load.objects.filter(class_pk=self.get_class())

    def save_edit_timetable(self):

        for lesson in self.get_lessons():

            get_new_lesson=self.request.POST.get("lesson"+str(lesson.pk))
            get_new_teacher=self.request.POST.get("teacher"+str(lesson.pk))
            
            if get_new_lesson and get_new_teacher:
                get_load=Load.objects.get(pk=get_new_lesson)
                get_teeacher=UserNet.objects.get(pk=get_new_teacher)
                lesson.teacher=get_teeacher
                lesson.subject_pk=get_load
                lesson.save()
            else:
                lesson.delete()


        return