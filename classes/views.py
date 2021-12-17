from django.contrib.auth.models import Group
from django.db import models
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import UpdateView, ListView, CreateView, DeleteView, View
from django.http import HttpResponseForbidden,HttpResponse
from user_account.models import UserNet
from user_account.permissions import AdminPermissionMixin
from .forms import *
from .models import *
from journal.models import *
from .utils import TimetableSettigns, CurruculumMixin
from institutions.permissions import InstitutionsMixin
from modules.users import get_user, generate_login
from modules.weeks import get_dates
import random
import re
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from journal.utils import Journal




class ClassView(PermissionRequiredMixin, CreateView):
    form_class = ClassForm
    template_name = 'classes/class.html'
    permission_required = 'classes.view_classes'
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
        subgroups_form=SubgroupsForm(class_number=class_info.class_number, profile=class_info.сurriculum)
        if request.method=="POST":
            if 'info' in request.POST:
                in_form=ClassForm(request.POST,instance=class_info,teacher=request.user.institution)
                if in_form.is_valid():
                    in_form.save()
                    messages.success(request, 'Информация обновлена!')
                    return redirect(request.META.get('HTTP_REFERER'))
            if 'subroups' in request.POST:
                sub_form=SubgroupsForm(request.POST,class_number=class_info.class_number, profile=class_info.сurriculum)
                sub_form.instance.class_pk=class_info
                if sub_form.is_valid():
                    sub_form.save()
                    return redirect(request.META.get('HTTP_REFERER'))
        class_subgroups=Subgroups.objects.filter(class_pk=pk)
        context={"form":info_form,'subroups':subgroups_form,'title':'Редактирование класса','subgroups':class_subgroups}
        return render(request,'classes/class_edit.html',context)
    
    else:
        return HttpResponseForbidden()

class SubgroupView(View,Journal):
    form_class = ClassForm
    template_name = 'classes/subgroup.html'
    def get_classes(self):
        

        if not self.request.user.groups.filter(name__in=['Администратор ОО']):
            return Classes.objects.filter(class_teacher=self.request.user).order_by('class_number','letter')
        else:
           
            return Classes.objects.filter(institution=self.request.user.institution).order_by('class_number','letter')
    def get_student(self):
        return Student.objects.filter(class_pk=self.get_class(),user__isnull=False,user__is_active=True).order_by('user')
    def get_class(self):


        try:
            if not self.request.user.groups.filter(name__in=['Администратор ОО']):

                class_info=self.get_classes().first()
            elif 'pk' in self.kwargs:
                class_info=Classes.objects.get(pk=self.kwargs['pk'])
            else:
                class_info=Classes.objects.filter(institution=self.request.user.institution).first()
        except Classes.DoesNotExist:
            class_info=None

        return class_info
    def get_subgroups(self):
        return Subgroups.objects.filter(class_pk=self.get_class())


    def get_context(self):
        context = {}
        context['title'] = 'Подгруппы '+str(self.get_class().class_number)+str(self.get_class().letter)+' класса'
        context['classes']=self.get_classes()
        context['students']=self.get_student()
        context['class']=self.get_class()
        context['subgroup_list']=self.get_subgroups()
        context['subgroups']=self.get_subgroups().distinct('subject_pk')
        return context

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name,self.get_context())

    def post(self, request, *args, **kwargs):
        
        print(self.get_class())
        for subgroup in self.get_subgroups().distinct('subject_pk'):
            subgroup_pk=subgroup.subject_pk.pk
            for student in self.get_student():
                student_pk=student.pk
                sub=self.request.POST.get("sub"+str(subgroup_pk)+str(student_pk))
                if sub:
                    select_sub=Subgroups.objects.get(pk=sub)
                    check_sub=StudentSubgroup.objects.filter(student=student_pk, subject=select_sub.subject_pk )
                    if check_sub:
                        
                        check_sub.update(subgroup=  sub )
                    else:
                        sub_save=StudentSubgroup.objects.create(student=student,  subgroup_id=sub,subject=select_sub.subject_pk)

        return redirect(request.META.get('HTTP_REFERER'))



class СurriculumView(ListView):
    model = Сurriculum
    template_name = 'classes/curriculum.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Учебные планы'
        context['curriculums'] = Сurriculum.objects.filter(
            institution=self.request.user.institution.pk,year=self.request.user.institution.year.pk)
        return context

class СurriculumCreateView(AdminPermissionMixin, CurruculumMixin, CreateView):
    form_class = СurriculumForm
    template_name = 'classes/add_curriculum.html'

    def get_context_data(self):

        context=super().get_context_data()
        context['title']='Добавление учебного плана'
        c_def=self.get_curriculum_context(title='Добавление учебного плана')
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        form.instance.institution_id = self.request.user.institution.pk
        form.instance.year_id = self.request.user.institution.year.pk


        return super().form_valid(form)

    def get_success_url(self):
        self.form_save()
        return reverse('Curriculum')

class СurriculumUpdateView(AdminPermissionMixin, CurruculumMixin, UpdateView):
    model=Сurriculum
    form_class = СurriculumForm
    template_name = 'classes/add_curriculum.html'
    def get_context_data(self):

        context=super().get_context_data()
        context['title']='Редактирование учебного плана'
        c_def=self.get_curriculum_context(title='Редактирование учебного плана')
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        form.instance.institution_id = self.request.user.institution.pk
        form.instance.year_id = self.request.user.institution.year.pk
        return super().form_valid(form)

    def get_success_url(self):
        self.form_save()
        return reverse('Curriculum')
class DeleteCurriculum(InstitutionsMixin,AdminPermissionMixin, DeleteView):
    template_name = 'institutions/curriculum.html'

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Сurriculum, id=id_)

    def get_success_url(self):
        return reverse('Curriculum')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



class LoadView(AdminPermissionMixin, TimetableSettigns, View):
    form_class = СurriculumForm
    template_name = 'classes/load.html'

    def get_success_url(self):
        return reverse('Load')

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

class TimetableTemplatesView(AdminPermissionMixin,TimetableSettigns,ListView):
    model = TimetableTemplates
    template_name = 'classes/timetable_templates.html'
    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Шаблоны расписания '+str(self.get_class().class_number)+str(self.get_class().letter)+' класса'
        context['class']=self.get_class()
        context['templates'] = TimetableTemplates.objects.filter(class_pk=self.get_class())
        context['curriculums'] = Сurriculum.objects.filter(
            institution=self.request.user.institution.pk,year=self.request.user.institution.year.pk)
        return context

class AddTimetableTemplate(AdminPermissionMixin, TimetableSettigns, View):
    template_name = 'classes/timetable_add_template.html'
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

class TimetableWeek(AdminPermissionMixin, TimetableSettigns, View):
    template_name = 'classes/timetable_weeks.html'

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
                            lesson_save=Lessons.objects.create(number=lesson.lesson,date=date_week,class_pk=self.get_class(),subject_pk=lesson.subject_pk,teacher=lesson.subject_pk.teacher)
        messages.success(request,'Уроки успешно распределены')
        return redirect(request.META.get('HTTP_REFERER'))
class EditLessons(AdminPermissionMixin,TimetableSettigns,View):
    template_name='classes/timetable_editlesson.html'

    def get(self,request,class_pk):
        context={}
        context['title']='Редактирование уроков'
        context['date']=self.get_date()
        context['lessons']=self.get_lessons()
        context['class']=self.get_class()
        context['loads']=self.get_loads()
        print(self.get_class())
        context['teachers']=UserNet.objects.filter(institution=request.user.institution,groups=2,is_active=True)
        return render(request, self.template_name, context)
    def post(self,request,class_pk):
        self.save_edit_timetable()

        return redirect(request.META.get('HTTP_REFERER'))
class DeleteLessons(AdminPermissionMixin, View):
    def get(self,request,class_pk):
        begin=request.GET.get("begin")
        end=request.GET.get("end")
        lesson=Lessons.objects.filter(class_pk=class_pk,date__gte=begin,date__lte=end).delete()
        return redirect(request.META.get('HTTP_REFERER'))


#Ученики
class StudentListView(PermissionRequiredMixin, ListView):
    paginate_by = 35
    model = Student
    template_name = 'classes/students.html'
    permission_required = 'classes.view_student'
    def query(self):
        surname=self.request.GET.get('surname')
        name=self.request.GET.get('name')
        middle_name=self.request.GET.get('middle_name')
        class_pk=self.request.GET.get('class_pk')
        return surname,name,middle_name,class_pk
    def get_class(self):
        if self.request.user.groups.filter(name__in=['Администратор ОО']):
            return Classes.objects.filter(institution=self.request.user.institution)
        else:
            return Classes.objects.filter(class_teacher=self.request.user)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Обучающиеся'
        context['surname']=self.query()[0]
        context['name']=self.query()[1]
        context['middle_name']=self.query()[2]
        if self.query()[3]:
            context['class_pk']=int(self.query()[3])
        context['classes']=self.get_class()
        return context

    def get_queryset(self):
        
        if self.query()[0] or self.query()[1] or self.query()[2]:
            users=UserNet.objects.filter(institution=self.request.user.institution, groups__name='Ученик', is_active=True, 
                last_name__iregex=r"[[:<:]]{0}".format(self.query()[0]), first_name__iregex=r"[[:<:]]{0}".format(self.query()[1])
                , middle_name__iregex=r"[[:<:]]{0}".format(self.query()[2])

                )

            
        else:
            users=UserNet.objects.filter(institution=self.request.user.institution, groups__name='Ученик', is_active=True)

        if self.query()[3]:
            students=Student.objects.filter(user__in=users,class_pk=self.query()[3]).order_by('user__last_name')
        else:
            students=Student.objects.filter(user__in=users, class_pk__in=self.get_class()).order_by('user__last_name')
        return students
class AddStudent(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = OldStudentForm
    template_name = 'user_account/user_update.html'
    permission_required = 'classes.add_student'
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
        context['file']=FileTemplates.objects.filter(name='Шаблон для импорта учеников').first()
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
                if last_name:
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
                    user_pk.groups.set([4])
                    arr.append([last_name,first_name,patronymic,gender,birth_day,login,password,user_pk.pk,class_find])
                    

        context['title']='Результат импорта'
        context['users']=arr
        return render(request,'user_account/import_result.html',context)



class StudentEditView(PermissionRequiredMixin,SuccessMessageMixin,View):
    model = Student
    form_class = StudentUserForm
    second_form_class = StudentForm


    template_name = 'classes/student.html'
    pk_url_kwarg = 'student_pk'
    success_message = 'Информация обновлена'
    error_message='Ошибка'
    permission_required = 'classes.change_student'
    login_url='login'

    def get_student(self):
        return Student.objects.get(pk=self.kwargs['student_pk'])

    def get(self,request, **kwargs):
        context = {}
        
        
        context['title'] = 'Личное дело учащегося'
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.get_student().user)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=self.get_student())

        return render(request, self.template_name, context)
    

    def post(self,request, **kwargs):


        if 'first_name' in request.POST:
            form=self.form_class(request.POST,request.FILES or None,instance=self.get_student().user)
            if form.is_valid():
                form.save()

        if 'class_pk' in request.POST:
            form2=self.second_form_class(request.POST,instance=self.get_student())
            if form2.is_valid():
                form2.save()
            
        return redirect(request.META.get('HTTP_REFERER'))

class Deduction(PermissionRequiredMixin,SuccessMessageMixin,View):
    permission_required = 'classes.delete_student'
    def post(self,request, **kwargs):
        date=self.request.POST.get("date")
        student=self.request.POST.get("pk")
        get_student=Student.objects.get(pk=student)
        get_student.user.is_active=False
        get_student.user.save()
        StudentShifting.objects.create(student=get_student, type_shift=2, date=date)
        return redirect(request.META.get('HTTP_REFERER'))
