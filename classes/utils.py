from classes.models import Classes, BellTimetable
from journal.models import Lessons
from .models import СurriculumSubject, Load
from modules.weeks import get_all_weeks, get_dates
from institutions.models import Periods, Subject
from user_account.models import UserNet
from datetime import datetime
from django.db.models import Q



class TimetableSettigns():
    def get_class(self):
        try:
            if 'class_pk' in self.kwargs:
                self.kwargs['pk']=self.kwargs['class_pk']
            if 'pk' in self.kwargs :
                class_info=Classes.objects.get(pk=self.kwargs['pk'])
            else:
                class_info=Classes.objects.filter(institution=self.request.user.institution, year=self.request.user.institution.year.pk).first()
        except Classes.DoesNotExist:
            class_info=None

        return class_info 

    def get_classes(self):
        return Classes.objects.filter(institution=self.request.user.institution, year=self.request.user.institution.year.pk).order_by('class_number','letter')
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


class CurruculumMixin:
    def get_curriculum_context(self,**kwargs):
        context=kwargs
        context = super().get_context_data()
        if self.request.user.institution.typeInstitutions.title == 'Профессиональная образовательная организация':
            context['class'] = [6, 7, 8, 9, 10]
            context['subjects'] = Subject.objects.filter(
            Q(institution=self.request.user.institution.pk) | Q(institution=None), type_org__title='Профессиональная образовательная организация').order_by('title')
        else:
            context['class'] = [10, 11]
            context['subjects'] = Subject.objects.filter(
            Q(institution=self.request.user.institution.pk) | Q(institution=None)).order_by('title')
        
        context['profile']=self.object
        return context
    def form_save(self):

        subjects = Subject.objects.filter(
            Q(institution=self.request.user.institution.pk) | Q(institution=None)).order_by('title')
        for subject in subjects:

            for a in range(12):
                hour = self.request.POST.get("h" + str(subject.id)+ "c" + str(a))
                if hour:

                    hour=float(hour.replace(',', '.'))
                    print(hour,a)
                else:
                    hour=None
                if hour is not None and hour>0:
                    try:
                        get_subject=СurriculumSubject.objects.filter(profile=self.object,
                                                                          class_number=a,
                                                                          subject=subject).first()
                        get_subject.hour=hour
                        get_subject.save()
                    except:
                        curriculum_subject = СurriculumSubject.objects.create(profile=self.object,
                                                                          class_number=a,
                                                                          subject=subject,
                                                                          hour=hour)
                else:
                    try:
                        get_subject=СurriculumSubject.objects.filter(profile=self.object,
                                                                          class_number=a,
                                                                          subject=subject).first()

                        get_subject.delete()
                    except:
                        pass