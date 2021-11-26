from django.shortcuts import render
from django.views.generic import View, ListView
from user_account.permissions import AdminPermissionMixin
from classes.models import Load, Classes, Student
from institutions.models import Periods, BellProfile
from django.http import HttpResponseForbidden,HttpResponse
from .models import *
from .utils import Journal,TimetableSettigns
from django.http import JsonResponse


class JournalView(View,Journal):
    
    template_name = 'journal/journal.html'
    


    def get(self, request, *args, **kwargs):

        context={}
        context['title'] = 'Журнал'
        if self.get_loads():
            
            context['loads']=self.get_loads()
            context['load_pk']=self.get_load()
            context['students']=self.get_student()
            date_start=self.get_period().first().start
            date_end=self.get_period().first().end
            context['lessons']=Lessons.objects.filter(subject_pk=self.get_load(),date__range=[date_start,date_end]).order_by("date")
            context['period']=self.get_period().first()
            context['periods']=self.get_period()
            context['classes']=self.get_classes()
            context['scores']=self.count_average_score()
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        context={}
        context['title'] = 'Журнал'
        context['lessons']=self.get_lessons()
        context['period']=self.get_period()
        context['periods']=Periods.objects.filter(profile=self.get_period().profile)
        context['loads']=self.get_loads()
        context['load_pk']=self.get_load()
        context['students']=self.get_student()
        context['classes']=self.get_classes()
        date_start=self.get_period().start
        date_end=self.get_period().end
        context['scores']=self.count_average_score()
        return render(request, self.template_name, context)

def check_period(self,load):

    get_load=Load.objects.get(pk=load)
    get_class=Classes.objects.get(pk=get_load.class_pk.pk)
    filter_periods=Periods.objects.filter(profile=get_class.period_profile)
    periods=[]
    for period in filter_periods:
        periods.append(period.pk)
    response = {
        'period':periods,

    }

    return JsonResponse(response)

class LessonTopics(View):
    def get(self, request, *args, **kwargs):
        load_pk=self.kwargs.get("load")
        load=Load.objects.get(pk=load_pk)
        period_pk=self.kwargs.get("period")
        period=Periods.objects.get(pk=period_pk)
        get_class=Classes.objects.get(pk=load.class_pk.pk)
        context={}
        context['title']='Темы уроков и дз'
        context['period']=period
        context['lessons']=Lessons.objects.filter(subject_pk=load).order_by("date")
        context['load']=load
        context['types']=LessonType.objects.all()
        context['BellProfile']=BellProfile.objects.get(pk=get_class.bell_profile.pk)
        return render(request,'journal/lesson_topics.html',context)

    def post(self,request,*args,**kwargs):
        load_pk=self.kwargs.get("load")
        load=Load.objects.get(pk=load_pk)
        period_pk=self.kwargs.get("period")
        period=Periods.objects.get(pk=period_pk)
        get_class=Classes.objects.get(pk=load.class_pk.pk)
        lessons=Lessons.objects.filter(subject_pk=load,date__range=[period.start,period.end])
        context={}
        context['title']='Темы уроков и дз'
        context['period']=period
        context['lessons']=Lessons.objects.filter(subject_pk=load).order_by("date")
        context['load']=load
        context['types']=LessonType.objects.all()
        context['BellProfile']=BellProfile.objects.get(pk=get_class.bell_profile.pk)
        for lesson in lessons:
            topic=request.POST.get("topic"+str(lesson.pk))
            homework=request.POST.get("homework"+str(lesson.pk))
            date_homework=request.POST.get("date_homework"+str(lesson.pk))
            types=request.POST.getlist("types"+str(lesson.pk))
            types_red=request.POST.getlist("typesRed"+str(lesson.pk))
            if types:
                for type_ in types:
                    if type_:
                        lesson.types.add(type_)
            
            if date_homework:
                get_lesson_homework=Lessons.objects.get(pk=date_homework)
                lesson.date_homework=get_lesson_homework
            lesson.homework=homework
            lesson.topic=topic
            lesson.save()

        return render(request,'journal/lesson_topics.html',context)


class Mark(View):
    def post(self,request,*args,**kwargs):
        mark=request.POST['mark']
        attendance=request.POST['attendance']
        student=request.POST['student']
        lesson_type=request.POST['type']
        lesson=request.POST['lesson']
        red_mark=request.POST['red_mark']
        del_mark=request.POST['del_mark']
        itog=request.POST['itog']
        is_itog=request.POST['isitog']
        get_student=Student.objects.get(pk=student)
        mark_pk=0
        if int(itog)==0:
            get_lesson=Lessons.objects.get(pk=lesson)
            get_lesson_type=LessonType.objects.get(pk=lesson_type)
            if int(red_mark)==0 and int(del_mark)==0:
                if int(mark)==0:
                    create_mark=Marks.objects.create(student=get_student,lesson=get_lesson,lesson_type=get_lesson_type,attendance=attendance)
                else:
                    create_mark=Marks.objects.create(student=get_student,lesson=get_lesson,lesson_type=get_lesson_type,mark=mark)
                mark_pk=create_mark.pk
            if int(red_mark)!=0 and int(del_mark)==0:
                get_mark=Marks.objects.get(pk=red_mark)
                if int(mark)==0:
                    get_mark.attendance=attendance
                    get_mark.mark=0
                else:
                    get_mark.mark=mark
                    get_mark.attendance=0
                get_mark.save()
                mark_pk=get_mark.pk
            
            if int(red_mark)==0 and int(del_mark)!=0:
                
                get_mark=Marks.objects.get(pk=del_mark)
                
                get_mark.delete()
        else:
            get_load=Load.objects.get(pk=lesson)
            period=Periods.objects.get(pk=itog)
            if int(red_mark)==0 and int(del_mark)==0:
                if int(is_itog)!=0:
                    period=None
                if int(mark)==0:
                    mark_pk=MarksItog.objects.create(student=get_student,not_certified=attendance,period=period,itog=is_itog,load=get_load)
                else:
                    
                    mark_pk=MarksItog.objects.create(student=get_student,mark=mark,period=period,itog=is_itog,load=get_load)
                mark_pk=mark_pk.pk
            if int(red_mark)!=0 and int(del_mark)==0:
                get_mark=MarksItog.objects.get(pk=red_mark)
                if int(mark)==0:
                    get_mark.not_certified=attendance
                    get_mark.mark=0
                else:
                    get_mark.mark=mark
                    get_mark.not_certified=0
                get_mark.save()
                mark_pk=get_mark.pk

            if int(red_mark)==0 and int(del_mark)!=0:
                get_mark=MarksItog.objects.get(pk=del_mark)
                
                get_mark.delete()

        return HttpResponse(mark_pk)
    def get(self,request,*args,**kwargs):
        return HttpResponse('Кукиш')



class ItogView(View,Journal):
    
    template_name = 'journal/itog.html'
    def get(self, request, *args, **kwargs):
        context={}
        context['title'] = 'Итоговые оценки'
        context['loads']=Load.objects.filter(teacher=request.user).order_by('class_pk','subject_pk')
        context['load_pk']=self.get_load()
        context['students']=self.get_student()
        date_start=self.get_period().first().start
        date_end=self.get_period().first().end
        context['period']=self.get_period().first()
        context['periods']=self.get_period()
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        context={}
        context['title'] = 'Итоговые оценки'
        date_start=self.get_period().start
        date_end=self.get_period().end
        context['period']=self.get_period()
        context['periods']=Periods.objects.filter(profile=self.get_period().profile)
        context['loads']=Load.objects.filter(teacher=request.user).order_by('class_pk','subject_pk')
        context['load_pk']=self.get_load()
        context['students']=Student.objects.filter(class_pk=self.get_class(),user__isnull=False).order_by('user')
        return render(request, self.template_name, context)

def get_loads(request,class_pk):
    
    loads=Load.objects.filter(class_pk__id=class_pk)
    load_list=[]
    urls=[]
    names=[]
    pk_array=[]
    for load in loads:
        load_list.append(load.pk)
        urls.append(load.periods())
        pk_array.append(str(load.pk))
        if load.subgroup:
            names.append(str(load.subject_pk.subject.title+' ('+load.subgroup.name+')'))
        else:
            names.append(str(load.subject_pk.subject.title))
    response = {
        'loads':load_list,
        'url':urls,
        'names':names,
        'pk_array':pk_array,
    }
    return JsonResponse(response)

