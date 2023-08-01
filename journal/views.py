from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, CreateView
from user_account.permissions import AdminPermissionMixin
from classes.models import Load, Classes, Student,StudentSubgroup, СurriculumSubject
from institutions.models import Periods, BellProfile, Subject
from django.http import HttpResponseForbidden, HttpResponse
from .models import *
from .utils import Journal, TimetableSettigns
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
import time
from datetime import date, timedelta, datetime
from django.db.models import Q
import json
from .forms import KTPForm, SectionsKTPForm
import csv
import codecs
from user_account.models import FileTemplates





class SchoolJournalView(View, Journal):
    template_name = 'journal/journal.html'
    type_journal='school'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context())

    def post(self, request, *args, **kwargs):
        
        
        return render(request, self.template_name, self.get_context())
        

class ClassesJournalView(View, Journal):
    template_name = 'journal/journal.html'
    type_journal='school'
    def get_classes(self):
        return Classes.objects.filter(class_teacher=self.request.user)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context())

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context())

class MyJournalView(View, Journal):
    template_name = 'journal/journal.html'
    type_journal='my'
    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, self.get_context())

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context())


def check_period(self, load):
    get_load = Load.objects.get(pk=load)
    get_class = Classes.objects.get(pk=get_load.class_pk.pk)
    filter_periods = Periods.objects.filter(profile=get_class.period_profile)
    periods = []
    num=0
    for period in filter_periods:
        periods.append(period.pk)
        if period.pk==Periods.objects.filter(profile=get_class.period_profile,end__gte=datetime.today()).first().pk:
            num=period.pk
    response = {
        'period': periods,
        'now_period':num

    }

    return JsonResponse(response)


class LessonTopics(View):

    def get_load(self, **kwargs):
        load = self.kwargs['load']
        return Load.objects.get(pk=load)
    def get(self, request, *args, **kwargs):
        self.referer = self.request.META.get('HTTP_REFERER')
        load_pk = self.kwargs.get("load")
        load = Load.objects.get(pk=load_pk)
        period_pk = self.kwargs.get("period")
        period = Periods.objects.get(pk=period_pk)
        get_class = Classes.objects.get(pk=load.class_pk.pk)
        context = {}
        context['title'] = 'Темы уроков и дз'
        context['period'] = period
        context['lessons'] = Lessons.objects.filter(subject_pk=load).order_by("date")
        context['load'] = load
        context['types'] = LessonType.objects.filter(Q(institution=request.user.institution) | Q(institution=None))
        context['BellProfile'] = BellProfile.objects.get(pk=get_class.bell_profile.pk)
        context['referer']=self.referer
        context['ktp'] = KTP.objects.filter(loads=load)
        return render(request, 'journal/lesson_topics.html', context)

    def post(self, request, *args, **kwargs):
        load_pk = self.kwargs.get("load")
        load = Load.objects.get(pk=load_pk)
        period_pk = self.kwargs.get("period")
        period = Periods.objects.get(pk=period_pk)
        get_class = Classes.objects.get(pk=load.class_pk.pk)
        lessons = Lessons.objects.filter(subject_pk=load).order_by('pk')
        ktp = KTP.objects.filter(loads=load)
        context = {}
        context['title'] = 'Темы уроков и дз'
        context['period'] = period
        context['lessons'] = Lessons.objects.filter(subject_pk=load).order_by("date")
        context['load'] = load
        context['types'] = LessonType.objects.all()
        context['BellProfile'] = BellProfile.objects.get(pk=get_class.bell_profile.pk)
        context['success']=True
        context['referer']=self.request.POST.get("referer")
        context['ktp'] = ktp
        if self.request.POST.get('upload_ktp'):
            get_topics = TopiCktp.objects.filter(section__ktp=ktp.first()).order_by('section','pk')
            arr = []
            for topic in get_topics:
                for i in range(0,topic.hour):
                    arr.append(topic)
            
            i = 0
            for lesson in lessons:
                if lesson.date >= period.start and lesson.date <= period.end and not lesson.ktp and len(arr)-1>=i:
                    lesson.topic = arr[i].name
                    lesson.homework = arr[i].homework
                    lesson.ktp = arr[i]
                    lesson.save()

                i+=1
        else:
            for lesson in lessons:
                topic = request.POST.get("topic" + str(lesson.pk))
                homework = request.POST.get("homework" + str(lesson.pk))
                date_homework = request.POST.get("date_homework" + str(lesson.pk))
                types = request.POST.getlist("types" + str(lesson.pk))
                types_red = request.POST.getlist("typesred" + str(lesson.pk))
                type_red_old = 0
                for type_red in types_red:
                    
                    type_p=type_red.split('/')
                    new_type=type_p[1]
                    old_type=type_p[0]
                    get_type=lesson.types.filter(pk=old_type).first()

                    if old_type!=new_type:
                        lesson.types.remove(get_type)
                        

                        if int(new_type)!=0:
                            lesson.types.add(new_type)
                        if type_red_old == new_type:
                            Marks.objects.filter(lesson=lesson,lesson_type__pk=old_type).delete()

                        Marks.objects.filter(lesson=lesson,lesson_type=get_type).update(lesson_type=new_type)
                        lesson.types.remove(get_type)
                    type_red_old = new_type

                for type_ in types:
                    if type_:
                        
                        lesson.types.add(type_)

                if date_homework:
                    get_lesson_homework = Lessons.objects.get(pk=date_homework)
                    lesson.date_homework = get_lesson_homework
                lesson.homework = homework
                lesson.topic = topic
                lesson.save()

        return render(request, 'journal/lesson_topics.html', context)


def returnview(request):
   
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class Mark(View):
    def post(self, request, *args, **kwargs):
        mark = request.POST['mark']
        two_mark=request.POST['two_mark']
        attendance = request.POST['attendance']
        student = request.POST['student']
        lesson_type = request.POST['type']
        lesson = request.POST['lesson']
        red_mark = request.POST['red_mark']
        del_mark = request.POST['del_mark']
        itog = request.POST['itog']
        is_itog = request.POST['isitog']
        get_student = Student.objects.get(pk=student)
        mark_pk = 0

        if int(itog) == 0:
            get_lesson = Lessons.objects.get(pk=lesson)
            get_lesson_type = LessonType.objects.get(pk=lesson_type)
            if int(red_mark) == 0 and int(del_mark) == 0:
                if int(mark) == 0:
                    
                    create_mark = Marks.objects.create(student=get_student, lesson=get_lesson,
                                                   lesson_type=get_lesson_type, attendance=attendance)
                else:
                    if int(two_mark)>0:
                        
                        create_mark = Marks.objects.create(student=get_student, lesson=get_lesson,
                                                       lesson_type=get_lesson_type, mark2=two_mark, mark=mark)
                    else:
                        create_mark = Marks.objects.create(student=get_student, lesson=get_lesson,
                                                       lesson_type=get_lesson_type, mark=mark)
                mark_pk = create_mark.pk
            if int(red_mark) != 0 and int(del_mark) == 0:
                get_mark = Marks.objects.get(pk=red_mark)
                if int(mark) == 0:
                    get_mark.attendance = attendance
                    get_mark.mark = 0
                else:
                    if int(two_mark)>0:
                        get_mark.mark2=two_mark

                    get_mark.mark = mark
                    get_mark.attendance = 0

                    if int(two_mark)==0:
                        get_mark.mark2=0
                get_mark.save()
                mark_pk = get_mark.pk

            if int(red_mark) == 0 and int(del_mark) != 0:
                get_mark = Marks.objects.get(pk=del_mark)

                get_mark.delete()
        else:
            get_load = Load.objects.get(pk=lesson)
            period = Periods.objects.get(pk=itog)
            if int(red_mark) == 0 and int(del_mark) == 0:
                if int(is_itog) != 0:
                    period = None
                if int(mark) == 0:
                    mark_pk = MarksItog.objects.create(student=get_student, not_certified=attendance, period=period,
                                                       itog=is_itog, load=get_load)
                else:

                    mark_pk = MarksItog.objects.create(student=get_student, mark=mark, period=period, itog=is_itog,
                                                       load=get_load)
                mark_pk = mark_pk.pk
            if int(red_mark) != 0 and int(del_mark) == 0:

                get_mark = MarksItog.objects.get(pk=red_mark)
                if int(mark) == 0:
                    get_mark.not_certified = attendance
                    get_mark.mark = 0
                else:
                    get_mark.mark = mark
                    get_mark.not_certified = 0
                if two_mark==0:
                    get_mark.mark2=0
                get_mark.save()
                mark_pk = get_mark.pk
            if int(red_mark) == 0 and int(del_mark) != 0:
                get_mark = MarksItog.objects.get(pk=del_mark)

                get_mark.delete()

        return HttpResponse(mark_pk)

    def get(self, request, *args, **kwargs):
        return HttpResponse('Кукиш')


class ItogView(View, Journal):
    template_name = 'journal/itog.html'
    def get_load(self, **kwargs):
        load = self.kwargs['load']
        return Load.objects.get(pk=load)
    def get(self, request, *args, **kwargs):
        context = {}
        context['title'] = 'Итоговые оценки'
        context['loads'] = Load.objects.filter(teacher=request.user).order_by('class_pk', 'subject_pk')
        context['load_pk'] = self.get_load()
        context['students'] = self.get_student()
        date_start = self.get_period().start
        date_end = self.get_period().end
        context['period'] = self.get_period()
        context['periods'] = Periods.objects.filter(profile=self.get_period().profile)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        context['title'] = 'Итоговые оценки'
        date_start = self.get_period().start
        date_end = self.get_period().end
        context['period'] = self.get_period()
        context['periods'] = Periods.objects.filter(profile=self.get_period().profile)
        context['loads'] = Load.objects.filter(teacher=request.user).order_by('class_pk', 'subject_pk')
        context['load_pk'] = self.get_load()
        context['students'] = Student.objects.filter(class_pk=self.get_class(), user__isnull=False).order_by('user')
        return render(request, self.template_name, context)


def get_loads(request, class_pk):
    loads = Load.objects.filter(class_pk__id=class_pk)
    load_list = []
    urls = []
    names = []
    pk_array = []
    for load in loads:
        load_list.append(load.pk)
        urls.append(load.periods())
        pk_array.append(str(load.pk))
        if load.subgroup:
            names.append(str(load.subject_pk.subject.title + ' (' + load.subgroup.name + ')'))
        else:
            names.append(str(load.subject_pk.subject.title))
    response = {
        'loads': load_list,
        'url': urls,
        'names': names,
        'pk_array': pk_array,
    }
    return JsonResponse(response)





class TeacherTimeatable(View):

    template_name='journal/timetable_tacher.html'

    def get(self,request):
        context={}
        context['title']='Мое расписание'

        day = datetime.today().strftime("%Y-%m-%d")
        dt = datetime.strptime(day, '%Y-%m-%d')
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        

        lessons=Lessons.objects.filter(teacher=request.user, date__range=[start,end])
        arr1={}
        changes=[[
            {},{},{},{},{},{},{}


        ],
        [
            {},{},{},{},{},{},{}


        ]
        ]

        
        for lesson in lessons:
            
            weekday=datetime.strptime(str(lesson.date), '%Y-%m-%d').weekday()
            
            changes[lesson.class_pk.change-1][lesson.number-1][weekday]=lesson

            
        
        context['lessons']=changes
        return render(request,self.template_name,context)



class DeleteTopics(View):
    def get(self,request,load,period):
        
        get_period=Periods.objects.get(pk=period)
        lessons=Lessons.objects.filter(date__gte=get_period.start, date__lte=get_period.end, subject_pk__pk=load)
        for lesson in lessons:
            lesson.topic=''
            lesson.homework=''
            lesson.ktp = None
            lesson.save()
        return redirect(request.META.get('HTTP_REFERER'))


class AttendanceJournal(View, Journal):
    template_name='journal/attendance.html'


    def get_classes(self):
        if self.request.user.has_perm('journal.change_marks'):
            return Classes.objects.filter(institution=self.request.user.institution).order_by('class_number','letter')
        else:
            return Classes.objects.filter(class_teacher=self.request.user)
    def get_class(self):


        try:

            if 'pk' in self.kwargs:
                class_info=Classes.objects.get(pk=self.kwargs['pk'])
            else:

                class_info=self.get_classes().first()
        except Classes.DoesNotExist:
            class_info=None

        return class_info

    def get_student(self):



        return Student.objects.filter(class_pk=self.get_class(),user__isnull=False,user__is_active=True).order_by('user')

    def days_cur_month(self):
        m = datetime.now().month
        y = datetime.now().year
        ndays = (date(y, m, 1) - date(y, m-1, 1)).days
        d1 = date(y, m, 1)
        d2 = date(y, m, ndays)
        delta = d2 - d1

        return [(d1 + timedelta(days=i)).strftime('%d') for i in range(delta.days + 1)],m,y

    def get_context(self):
        context={}

        context['title']='Журнал посещаемости'
        context['classes']=self.get_classes()
        context['class']=self.get_class()
        context['students']=self.get_student()
        context['dates']=self.days_cur_month()[0]
        context['month']=self.days_cur_month()[1]
        context['year']=self.days_cur_month()[2]

        return context
    def get(self,request, *args,**kwargs):

        return render(request,self.template_name,self.get_context())


def get_lessons_attendance(request):

    month=int(request.GET.get('month'))
    day=int(request.GET.get('date'))
    year=int(request.GET.get('year'))
    student=int(request.GET.get('student'))
    subroups=list(StudentSubgroup.objects.filter(student_id=student).values_list('subgroup',flat=True))
    
    class_pk=(request.GET.get('class'))
    date_lessons=datetime(year,month,day).strftime('%Y-%m-%d')
    lessons=Lessons.objects.filter( Q(subject_pk__subgroup__in=subroups) | Q(subject_pk__subgroup=None),class_pk=class_pk, date=date_lessons )
    lesson_array=[]
    pk_array=[]
    mark_array=[]
    attendance=0
    for lesson in lessons:
        lesson_array.append(lesson.subject_pk.subject_pk.subject.short_title)
        pk_array.append(lesson.pk)
    for mark in Marks.objects.filter(student_id=student,lesson__in=lessons,attendance=1).distinct():


        mark_array.append(mark.lesson.pk)
        

    response={
        'lessons':lesson_array,
        'pks':pk_array,
        'marks':mark_array,
    }

   
    return JsonResponse(response)




def save_lessons_attendance(request):

    student=int(request.POST.get('student'))
    get_student=Student.objects.get(pk=student)
    lessons=request.POST.get('lessons')
    lessons=json.loads(lessons)

    delete=request.POST.get('delete')
    delete=json.loads(delete)


    



    for lesson in lessons:
        get_lesson=Lessons.objects.get(pk=lesson)
        types=get_lesson.types.all()
        for type_ in types:
            marks_get=Marks.objects.filter(student=get_student, lesson=get_lesson, lesson_type=type_,attendance=1)
            if not marks_get:
                Marks.objects.create(student=get_student, lesson=get_lesson, lesson_type=type_,attendance=1)



    if delete:
        for lesson in delete:
            get_lesson=Lessons.objects.get(pk=lesson)
            if get_lesson:
                types=get_lesson.types.all()
                for type_ in types:
                    marks_get=Marks.objects.filter(student=get_student, lesson=get_lesson, lesson_type=type_,attendance=1)
                    marks_get.delete()


    response={
        'lessons':1,
        
    }

   
    return JsonResponse(response)

def save_reason(request):

    reason=request.GET.get('reason')
    month=int(request.GET.get('month'))
    day=int(request.GET.get('day'))
    year=int(request.GET.get('year'))
    student=int(request.GET.get('student'))
    student=Student.objects.get(pk=student)
    date=datetime(year,month,day).strftime('%Y-%m-%d')
    ReasonSkipping.objects.create(reason=reason, student=student, day=date)

    return HttpResponse()



#КТП



class List_KTP(CreateView):
    template_name = 'journal/ktp_list.html'
    form_class = KTPForm
    def query(self, *args, **kwargs):

        if self.request.GET.get('subject'):
            author = self.request.GET.get('author')
            class_pk = self.request.GET.get('class')
            subject = self.request.GET.get('subject')
            return author,class_pk, subject
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        authors = UserNet.objects.filter(institution=self.request.user.institution,groups__name='Учитель',is_active=True)
        ktp = None
        classes = [
            1,2,3,4,5,6,7,8,9,10,11
        ]
        get_subject = Subject.objects.filter(Q(institution=self.request.user.institution) | Q(institution=None))

        if self.query():
            if int(self.query()[0])==0:
                ktp = KTP.objects.filter(institution=self.request.user.institution, class_number=self.query()[1], subject_ktp__pk=self.query()[2])
            else:
                ktp = KTP.objects.filter(institution=self.request.user.institution, class_number=self.query()[1], subject_ktp__pk=self.query()[2], author=self.query()[0] )
        else:
            ktp = KTP.objects.filter(institution=self.request.user.institution, class_number=1, subject_ktp=get_subject.first())

        context['title'] = 'Календарно-тематическое планирование (КТП)'
        context['classes'] = classes
        context['subjects'] = get_subject
        context['teachers'] = authors
        context['form'] = self.form_class()
        if self.query():
            context['author'] = int(self.query()[0])
            context['class'] = int(self.query()[1])
            context['subject'] = int(self.query()[2])
        context['ktp_list'] = ktp
        return context
    def form_valid(self, form):
        form.instance.institution_id = self.request.user.institution.pk
        form.instance.year = self.request.user.institution.year
        form.instance.author=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('KTP_pk', kwargs={'pk':self.object.pk})


class KTPView(View):
    template_name = 'journal/ktp_view.html'
    form_class = SectionsKTPForm



    def get(self,request, *args, **kwargs):
        ktp_get = KTP.objects.get(pk=self.kwargs['pk'])
        sections_ktp = Sections_KTP.objects.filter(ktp=ktp_get).order_by('pk')
        get_ktp_classes = KTP.objects.filter(class_number=ktp_get.class_number, subject_ktp=ktp_get.subject_ktp)
        loads = Load.objects.filter(class_pk__class_number=ktp_get.class_number, subject_pk__subject=ktp_get.subject_ktp).order_by('class_pk')
        context = {
            'title': 'Просмотр КТП',
            'ktp': ktp_get, 
            'form': self.form_class,
            'sections_ktp': sections_ktp, 
            'loads': loads,
            'ktps': get_ktp_classes,
            'file':FileTemplates.objects.filter(name='Шаблон для импорта ктп').first()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        ktp_get = KTP.objects.get(pk=self.kwargs['pk'])
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.ktp = ktp_get
            form.save()
        else:
            ktp_get = KTP.objects.get(pk=self.kwargs['pk'])
            load_get = request.POST.getlist('loads')
            ktp_get.loads.set(load_get,clear=True)

            get_sections = Sections_KTP.objects.filter(ktp=ktp_get)
            for section in get_sections:
                i = 0
                get_themes = request.POST.getlist('section' + str(section.pk))
                get_homeworks = request.POST.getlist('homeworks' + str(section.pk))
                get_hours = request.POST.getlist('hours' + str(section.pk))
                for theme in get_themes:
                    if theme!='':
                        TopiCktp.objects.create(name=get_themes[i], section=section, hour=get_hours[i],homework=get_homeworks[i])
                    i = i+1
            edit_topics = self.request.POST.getlist('topics')
            edit_hours = self.request.POST.getlist('hours')
            edit_homeworks = self.request.POST.getlist('homeworks')
            pks = self.request.POST.getlist('ids')
            if pks:
                a=0
                
                for i in pks:
                    i = int(i)
                    get_topic = TopiCktp.objects.get(pk=i)
                    get_topic.name = edit_topics[a]
                    get_topic.hour = int(edit_hours[a])
                    get_topic.homework = edit_homeworks[a]
                    get_topic.save()
                    a+=1
                    

        if 'import' in request.POST:
            file = request.FILES['file']
            # f = open(uploaded_file_url, 'rt',encoding='utf8')

            myreader = csv.DictReader(codecs.iterdecode(file, 'utf-8'))
            section_old = ''
            section = None
            for row in myreader:
                section_name = row['Разделы']
                topic = row['Темы уроков']
                hour = row['Количество часов']
                homework = row['Домашнее задание']
                if section_name!=section_old and section_name!='':
                    
                    section = Sections_KTP.objects.create(ktp=ktp_get, name=section_name)
                
                if (topic and hour)!='':
                    TopiCktp.objects.create(name=topic, hour=hour,section=section, homework=homework)
                section_old = row['Разделы']
        return redirect(request.META.get('HTTP_REFERER'))