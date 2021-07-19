from django.contrib.auth.models import Group
from django.db import models
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import UpdateView, ListView, CreateView, DeleteView, View
from user_account.models import UserNet
from user_account.permissions import AdminPermissionMixin
from .forms import *
from .models import *
from journal.models import *
from institutions.permissions import InstitutionsMixin
from multi_form_view import MultiFormView
from django.http import HttpResponseForbidden,HttpResponse
from modules.weeks import get_all_weeks, get_dates
from modules.users import get_user, generate_login
import random
import re


class ClassView(AdminPermissionMixin, CreateView):
    form_class = ClassForm
    template_name = 'classes/class.html'

    def get_success_url(self):
        return reverse('Class')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Классы'
        context['classes'] = Classes.objects.filter(
                institution=self.request.user.institution.pk,year=self.request.user.institution.year.pk)
        return context

    def get_form_kwargs(self):
        kwargs = super(ClassView, self).get_form_kwargs()
        kwargs['edit'] = True
        kwargs['teacher']=self.request.user.institution
        return kwargs


    def form_valid(self, form):
        form.instance.institution_id = self.request.user.institution.pk
        form.instance.year_id = self.request.user.institution.year.pk
        return super().form_valid(form)

def class_edit_view(request,pk):
    class_info=Classes.objects.get(pk=pk)
    if class_info.institution.pk==request.user.institution.pk:
        info_form=ClassForm(instance=class_info,teacher=request.user.institution)
        subgroups_form=SubgroupsForm(class_number=class_info.class_number)
        if request.method=="POST":
            if 'info' in request.POST:
                in_form=ClassForm(request.POST,instance=class_info,teacher=request.user.institution)
                if in_form.is_valid():
                    in_form.save()
                    messages.success(request, 'Информация обновлена!')
                    return redirect(request.META.get('HTTP_REFERER'))
            if 'subroups' in request.POST:
                sub_form=SubgroupsForm(request.POST,class_number=class_info.class_number)
                sub_form.instance.class_pk=class_info
                if sub_form.is_valid():
                    sub_form.save()
                    return redirect(request.META.get('HTTP_REFERER'))
        class_subgroups=Subgroups.objects.filter(class_pk=pk)
        context={"form":info_form,'subroups':subgroups_form,'title':'Редактирование класса','subgroups':class_subgroups}
        return render(request,'classes/class_edit.html',context)
    
    else:
        return HttpResponseForbidden()
class СurriculumView(ListView):
    model = Сurriculum
    template_name = 'classes/сurriculum.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Учебные планы'
        context['curriculums'] = Сurriculum.objects.filter(
            institution=self.request.user.institution.pk,year=self.request.user.institution.year.pk)
        return context

class СurriculumCreateView(AdminPermissionMixin, CreateView):
    form_class = СurriculumForm
    template_name = 'classes/add_curriculum.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Добавление учебных планов'
        context['class'] = [10, 11]
        context['subjects'] = Subject.objects.filter(
            Q(institution=self.request.user.institution.pk) | Q(institution=None)).order_by('title')
        return context

    def form_valid(self, form):
        form.instance.institution_id = self.request.user.institution.pk
        form.instance.year_id = self.request.user.institution.year.pk

        сurriculum_profile = form.save()
        subjects = Subject.objects.filter(
            Q(institution=self.request.user.institution.pk) | Q(institution=None)).order_by('title')
        for subject in subjects:

            for a in range(12):
                hour = self.request.POST.get("h" + str(subject.id) + str(a))
                if hour:
                    curriculum_subject = СurriculumSubject.objects.create(profile=сurriculum_profile,
                                                                          class_number=a,
                                                                          subject=subject,
                                                                          hour=hour)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Curriculum')


class LoadView(AdminPermissionMixin, View):
    form_class = СurriculumForm
    template_name = 'classes/load.html'

    def get_success_url(self):
        return reverse('Load')
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
    def get(self, request, *args, **kwargs):
        context = {}
        context['subjects'] = self.get_info()
        context['teachers']=UserNet.objects.filter(institution=self.request.user.institution.pk,groups=2,is_active=True).distinct()
        context['classes']=Classes.objects.filter(institution=self.request.user.institution.pk)
        context['class']=self.get_class()
        context['title'] = 'Учебная нагрузка'
        return render(request, self.template_name,context)
    def post(self, request, *args, **kwargs):
        subjects_list=self.get_info()
        class_pk=self.get_class().pk
        for subject in subjects_list:
            subroups_list=Subgroups.objects.filter(class_pk=class_pk,subject_pk=subject.pk)
            if subroups_list:
                for subgroup in subroups_list:
                    teacher=self.request.POST.get("subject_"+str(subject.pk)+"_subgroup_"+str(subgroup.pk))
                    load_check=Load.objects.filter(class_pk=class_pk,subject_pk=subject,subgroup=subgroup)
                    if load_check and teacher:
                        for i in load_check: get_teacher=i.pk
                        teacher_get=UserNet.objects.get(pk=teacher)
                        get_load=Load.objects.get(pk=get_teacher)
                        get_load.teacher=teacher_get
                        get_load.save()
                    else:
                        if teacher:
                            teacher_load=UserNet.objects.get(pk=teacher)
                            Load.objects.create(class_pk=self.get_class(),subject_pk=subject,subgroup=subgroup,teacher=teacher_load)
            else:
                teacher=self.request.POST.get("subject_"+str(subject.pk))
                load_check=Load.objects.filter(class_pk=class_pk,subject_pk=subject)
                if load_check and teacher:
                    for i in load_check: get_teacher=i.pk
                    teacher_get=UserNet.objects.get(pk=teacher)
                    get_load=Load.objects.get(pk=get_teacher)
                    get_load.teacher=teacher_get
                    get_load.save()
                else:
                    if teacher:
                        teacher_load=UserNet.objects.get(pk=teacher)
                        Load.objects.create(class_pk=self.get_class(),subject_pk=subject,teacher=teacher_load)
        return redirect(request.META.get('HTTP_REFERER'))


#Расписание
class Timetable(AdminPermissionMixin,ListView):
    model = Classes
    template_name = 'classes/timetable_classes.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Расписание'
        context['classes'] = Classes.objects.filter(institution=self.request.user.institution.pk)
        return context

class TimetableTemplatesView(AdminPermissionMixin,ListView):
    model = TimetableTemplates
    template_name = 'classes/timetable_templates.html'
    def get_class(self):
        return Classes.objects.get(pk=self.kwargs['pk'])
    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Шаблоны расписания '+str(self.get_class().class_number)+str(self.get_class().letter)+' класса'
        context['class']=self.get_class()
        context['templates'] = TimetableTemplates.objects.filter(class_pk=self.get_class())
        context['curriculums'] = Сurriculum.objects.filter(
            institution=self.request.user.institution.pk,year=self.request.user.institution.year.pk)
        return context

class AddTimetableTemplate(AdminPermissionMixin, View):
    template_name = 'classes/timetable_add_template.html'
    def get_class(self):
        return Classes.objects.get(pk=self.request.POST.get("class"))
    def post(self,request):
        context={}
        context['days'] = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        context['title'] = 'Добавление шаблона расписания'
        context['loads']=Load.objects.filter(class_pk=self.request.POST.get("class"))
        context['class_pk']=self.request.POST.get("class")
        return render(request, self.template_name,context)

class CreateTimetableTemplate(AdminPermissionMixin,View):

    def post(self,request):
        class_pk=request.POST.get("class_pk")
        class_get=Classes.objects.get(pk=class_pk)
        bell_filter=BellTimetable.objects.filter(profile=class_get.bell_profile).order_by('day','lesson')
        profile_name=request.POST.get("profile")
        template=TimetableTemplates.objects.create(сurriculum=class_get.сurriculum,name=profile_name,class_pk=class_get)
        for bell in bell_filter:
            lesson=bell
            loads=request.POST.getlist(str(bell.day)+str((bell.lesson)))
            
            for load in loads:
                if load:
                    get_subject=Load.objects.get(pk=int(load))
                    SubjectTemplate.objects.create(day=bell.day,lesson=bell.lesson,profile=template,subject_pk=get_subject)

        return redirect(class_get.timetable_templates())


class UpdateTimetableTemplate(AdminPermissionMixin,View):
    template_name = 'classes/timetable_add_template.html'
    def get_template(self):
        return TimetableTemplates.objects.get(pk=self.kwargs['pk'])
    def get(self, request, *args, **kwargs):
        context={}
        context['class_pk']=self.get_template().class_pk.pk
        context['template']=self.get_template()
        context['loads']=Load.objects.filter(class_pk=self.get_template().class_pk.pk)
        context['days'] = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        context['title'] = 'Редактирование'+'"'+self.get_template().name+'"'

        return render(request, self.template_name,context)
    def post(self,request,*args, **kwargs):
        class_pk=request.POST.get("class_pk")
        class_get=Classes.objects.get(pk=class_pk)
        bell_filter=BellTimetable.objects.filter(profile=class_get.bell_profile).order_by('day','lesson')
        profile_name=request.POST.get("profile")
        template=TimetableTemplates.objects.get(pk=self.get_template().pk)
        template.name=profile_name
        template.save()

        i=0

        get_template_subjects=SubjectTemplate.objects.filter(profile=template)
        for subject in get_template_subjects:
            loads=request.POST.getlist(str(subject.day)+str((subject.lesson)))
            if str(subject.subject_pk.pk) not in loads:

                get_template_subject=SubjectTemplate.objects.get(pk=subject.id).delete()

        for bell in bell_filter:
            lesson=bell
            loads=request.POST.getlist(str(bell.day)+str((bell.lesson)))
            new_loads=list(filter(None, loads))
            for load in new_loads:
                 check_template_subjects=SubjectTemplate.objects.filter(day=bell.day,lesson=bell.lesson,profile=template,subject_pk__id=load).values_list('subject_pk')
                 if check_template_subjects:
                    sub_template=check_template_subjects[0][0]
                 else:
                        get_subject=Load.objects.get(pk=int(load))
                        SubjectTemplate.objects.create(day=bell.day,lesson=bell.lesson,profile=template,subject_pk=get_subject)


        return redirect(class_get.timetable_templates())

class TimetableWeek(AdminPermissionMixin,View):
    template_name = 'classes/timetable_weeks.html'
    def get_class(self):
        return Classes.objects.get(pk=self.kwargs['pk'])
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
    def get(self, request, *args, **kwargs):
        context={}
        context['class_pk']=self.get_class()
        profile=PeriodProfile.objects.get(pk=self.get_class().period_profile.pk)
        if profile.typePeriod==4:
            context['name_period']='Четверть'
        elif profile.typePeriod==3:
            context['name_period']='Триместр'
        elif profile.typePeriod==2:
            context['name_period']='Полугодие'
        if 'period' in self.kwargs:
            context['period_pk']=self.kwargs['period']
        context['class']=self.get_class()
        context['templates']=TimetableTemplates.objects.filter(class_pk=self.get_class())
        context['weeks']=self.get_weeks()
        context['periods']=Periods.objects.filter(profile=self.get_class().period_profile)
        context['title'] = 'Распределение уроков '+str(self.get_class().class_number)+str(self.get_class().letter)+' класса'
        return render(request, self.template_name,context)
    def post(self, request, *args, **kwargs):
        context={}
        context['class_pk']=self.get_class()
        profile=PeriodProfile.objects.get(pk=self.get_class().period_profile.pk)
        i=0
        for week in self.get_weeks():
            i+=1
            post_week=request.POST.get(str('template')+str(i))
            if post_week:
                start=week[0]
                end=week[1]
                dates=get_dates(start,end)
                for date_week in dates:
                    if date_week>=self.get_period().start and date_week<=self.get_period().end:
                        weekday=date_week.isoweekday()
                        get_lesson=SubjectTemplate.objects.filter(profile__id=post_week,day=weekday)
                        for lesson in get_lesson:
                            lesson_save=Lessons.objects.create(number=lesson.lesson,date=date_week,class_pk=self.get_class(),subject_pk=lesson.subject_pk)
        messages.success(request,'Уроки успешно распределены')
        return redirect(request.META.get('HTTP_REFERER'))

#Ученики
class StudentListView(AdminPermissionMixin, ListView):
    model = Student
    template_name = 'classes/students.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Обучающиеся'
        users=UserNet.objects.filter(institution=self.request.user.institution, groups=3)
        context['users']=Student.objects.filter(user__in=users)
        return context
class AddStudent(AdminPermissionMixin, SuccessMessageMixin, CreateView):
    form_class = StudentForm
    template_name = 'user_account/user_update.html'
    def get_form_kwargs(self):
        kwargs = super(AddStudent, self).get_form_kwargs()
        kwargs['user'] =self.request.user
        return kwargs
    def form_valid(self, form):
        chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        self.login = ''
        self.password = ''
        for i in range(8):
            self.password += random.choice(chars)
        for i in range(8):
            self.login += random.choice(chars)
        user = form.save(commit=False)        
        user.set_password(self.password)
        user.username=self.login
        user.institution_id = self.request.user.institution.pk

        user.save()
        user.groups.add(3)
        Student.objects.create(user=user,class_pk=form.cleaned_data['class'])
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Добавление обучающегося'
        return context

    def get_success_url(self):
        return reverse('StudentList')
    def get_success_message(self, cleaned_data):
        ms = "Логин:" + self.login + "\n" + "Пароль:" + self.password
        success_message = ms
        return success_message % cleaned_data

class ImportStudent(View):
    def get(self,request):
        context={}
        context['title']='Импорт пользователей'
        context['file']=FileTemplates.objects.filter(name='Шаблон для импорта пользователей').first()
        return render(request,'classes/import_user.html',context)
    def post(self,request):
        context={}

        if 'add' in request.POST:
            get_users=request.POST.getlist("users")
            get_classes=request.POST.getlist("users_classes")
            
            i=0
            for user in get_users:
                user_get=UserNet.objects.get(pk=user)
                user_get.is_active=True
                user_get.save()
                pk_class=get_classes[i]
                get_class=Classes.objects.get(pk=pk_class)
                Student.objects.create(user=user_get,class_pk=get_class)
                i+=1
            messages.success(request, 'Учащиеся успешно импортированы!')
            return redirect('ImportUser')
        else:
            file=request.FILES['file']
            users=get_user(file)
            arr=[]
            for row in range(2,users.max_row+1):
                last_name=users[row][0].value
                first_name=users[row][1].value
                patronymic=users[row][2].value
                gender=users[row][3].value
                birth_day=users[row][4].value
                class_=users[row][5].value
                letter=re.sub("[0-9]", "", class_)
                class_=class_.rsplit('-')
                class_ = "".join(c for c in class_[0] if  c.isdecimal())
                class_find=Classes.objects.filter(institution=request.user.institution,class_number=class_,letter=letter).first()
                login=generate_login()[0]
                password=generate_login()[1]
                user_pk=UserNet.objects.create_user(is_active=False,username=login,password=password,last_name=last_name,first_name=first_name,middle_name=patronymic,gender=gender,birth_day=birth_day,institution=self.request.user.institution)
                user_pk.groups.set([3])
                arr.append([last_name,first_name,patronymic,gender,birth_day,login,password,user_pk.pk,class_find])
                    

        context['title']='Результат импорта'
        context['users']=arr
        return render(request,'user_account/import_result.html',context)