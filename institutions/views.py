import random
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import UpdateView, ListView, CreateView, DeleteView, View
from user_account.models import UserNet
from user_account.permissions import AdminPermissionMixin
from .forms import *
from .models import *
from .permissions import InstitutionsMixin
from .utils import Study_Periods
from django.contrib.auth.mixins import PermissionRequiredMixin
from journal.models import LessonType
from classes.models import Classes, Student


class InstitutionsHomeView(PermissionRequiredMixin,SuccessMessageMixin, View):
    model = Institutions
    form_class = InstitutionsInfoForm
    second_form_class=TypeLesson
    template_name = 'institutions/institutions.html'
    success_message = 'Информация об организации успешно обновлена!'
    permission_required = 'institutions.view_institutions'
    


    def get(self,request, **kwargs):
        context = {}
        
        
        context['title'] = 'Настройки организации'
        context['types']=LessonType.objects.filter(Q(institution=request.user.institution) | Q(institution=None))
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.get_object())

        if 'form2' not in context:
            context['form2'] = self.second_form_class()


        return render(request, self.template_name, context)
    

    def post(self,request, **kwargs):


        if 'title' in request.POST:
            form=self.form_class(request.POST,request.FILES or None,instance=self.get_object())
            if form.is_valid():
                form.save()

        if 'name' in request.POST:
            form2=self.second_form_class(request.POST,)
            if form2.is_valid():
                form2.instance.institution=request.user.institution
                form2.save()
            
        return redirect(request.META.get('HTTP_REFERER'))


    def get_object(self, **kwargs):
        return Institutions.objects.get(pk=self.request.user.institution.pk)


class AdsCreateView(CreateView):

    form_class=AdsForm
    template_name='institutions/ads.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = "Объявления"
        context['ads']=AdsInstitution.objects.filter(institution=self.request.user.institution)
        return context
    def form_valid(self, form):
        form.instance.institution_id = self.request.user.institution.pk
        form.instance.author=self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('create_ad')

class AdsDeleteView(View):
    

    def get(self, request, *args, **kwargs):
        id_ = self.kwargs.get("pk")
        AdsInstitution.objects.get(pk=id_).delete()
        return redirect(request.META.get('HTTP_REFERER'))


class StudyPeriodsView(PermissionRequiredMixin,ListView):
    model = PeriodProfile
    template_name = 'institutions/study_periods.html'
    permission_required = 'institutions.view_periodprofile'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        period_profile = PeriodProfile.objects.filter(institution=self.request.user.institution.pk,year=self.request.user.institution.year.pk)
        context['period_profile'] = period_profile
        context['title'] = "Профили учебных периодов"
        return context


class Add_periods(AdminPermissionMixin, CreateView):
    form_class = PeriodsForm
    template_name = 'institutions/add_periods.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = "Добавление учебного периода"
        return context

    def form_valid(self, form):
        form.instance.typePeriod = self.request.POST.get("type_period")
        form.instance.institution_id = self.request.user.institution.pk
        form.instance.year_id = self.request.user.institution.year.pk
        type_period = self.request.POST.get("type_period")
        period_profile = form.save(commit=False)
        period_profile.save()
        profile_pk = period_profile
        one_start = self.request.POST.get("one_start")
        one_end = self.request.POST.get("one_end")
        one_period = Periods.objects.create(profile=profile_pk, start=one_start, end=one_end)
        two_start = self.request.POST.get("two_start")
        two_end = self.request.POST.get("two_end")
        two_period = Periods.objects.create(profile=profile_pk, start=two_start, end=two_end)

        if int(type_period) == 3 or int(type_period) == 4:
            three_start = self.request.POST.get("three_start")
            three_end = self.request.POST.get("three_end")
            three_period = Periods.objects.create(profile=profile_pk, start=three_start, end=three_end)
        if int(type_period) == 4:
            four_start = self.request.POST.get("four_start")
            four_end = self.request.POST.get("four_end")
            four_period = Periods.objects.create(profile=profile_pk, start=four_start, end=four_end)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('StudyPeriods')


class DeleteProfilePeriods(InstitutionsMixin,AdminPermissionMixin, DeleteView):
    template_name = 'institutions/study_periods.html'

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(PeriodProfile, id=id_)

    def get_success_url(self):
        return reverse('StudyPeriods')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class StudyPeriodsUpdateView(View, Study_Periods):
    template_name = 'institutions/study_periods_edit.html'
    def get(self,request,profile_pk):
        context={}
        context['title']='Редактирование учебных периодов'
        context['periods']=self.get_periods()
        context['period_profile']=self.get_period_profile()
        return render(request,self.template_name,context)
    def post(self,request,profile_pk):
        self.get_update_period()

        return redirect('StudyPeriods')

#Звонки
class BellProfileView(AdminPermissionMixin, ListView):
    model = BellProfile
    template_name = 'institutions/bell_profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = "Профили звонков"
        context['bell_profiles'] = BellProfile.objects.filter(institution=self.request.user.institution.pk)
        return context


class BellProfileCreateView(AdminPermissionMixin, CreateView):
    form_class = BellForm
    template_name = 'institutions/bell_profile_create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = "Добавление профиля звонков периода"
        context['days'] = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        return context

    def form_valid(self, form):
        bell_profile = form.save(commit=False)
        form.instance.institution_id = self.request.user.institution.pk
        bell_profile.save()
        profile = bell_profile
        n = 8
        a = 0
        while a <= 5:
            a += 1
            for i in range(n):
                i += 1
                bell_start = self.request.POST.get("b" + str(a) + str(i))
                bell_end = self.request.POST.get("e" + str(a) + str(i))
                if bell_start and bell_end:
                    bell_period = BellTimetable.objects.create(profile=bell_profile, start=bell_start, end=bell_end,
                                                               day=a, lesson=i)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Bell_profile_list')


class SubjectView(AdminPermissionMixin, CreateView):
    form_class = SubjectForm
    template_name = 'institutions/subject_list.html'

    def form_valid(self, form):
        form.instance.institution_id = self.request.user.institution.pk
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Учебные предметы'
        context['subjects'] = Subject.objects.filter(
            Q(institution=self.request.user.institution.pk) | Q(institution=None)).order_by('title')
        context['institution']=self.request.user.institution
        return context

    def get_success_url(self):
        return reverse('Subject_list')


class DeleteSubject(InstitutionsMixin, DeleteView):
    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Subject, id=id_)

    def get_success_url(self):
        return reverse('Subject_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

#Админка ###############################################################################
class InstitutionCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = InstitutionForm
    template_name = 'institutions/institutions_create.html'
    permission_required='institutions.add_institutions'

    def get_types(self):
        
        if self.request.user.is_superuser:
            types=TypeInstitutions.objects.all()
        elif self.request.user.institution.typeInstitutions.title == 'Орган управления':
            types=TypeInstitutions.objects.filter(title='Образовательная организация')
        return types

    def get_departmental(self):
        

        if self.request.user.is_superuser == True:
            departmentals=Institutions.objects.filter(typeInstitutions__title='Орган управления')
        else:
            departmentals=Institutions.objects.filter(typeInstitutions__title='Орган управления', pk = self.request.user.institution.pk)
        return departmentals

    def get_form_kwargs(self):
        kwargs = super(InstitutionCreate, self).get_form_kwargs()
        kwargs['types']=self.get_types().values_list('pk')
        return kwargs

    def form_valid(self, form):
        chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        self.login = ''
        self.password = ''
        institutions_create = form.save()
        for i in range(8):
            self.password += random.choice(chars)
        for i in range(8):
            self.login += random.choice(chars)
        group = TypeInstitutions.objects.get(pk=self.request.POST.get("typeInstitutions")).group.all()[0]
        user = UserNet.objects.create_user(username=self.login, password=self.password,
                                           institution=institutions_create)
        user.groups.set([group])

        return super().form_valid(form)

    def query(self):

        short_title=self.request.GET.get('short_title')
        ban=self.request.GET.get("ban")
        if (short_title or ban) is not None:
            return short_title,ban


    def get_institution(self):
        if self.request.user.is_superuser == True:
            department_q = Q(departmental_organization__in=self.get_departmental()) | Q(departmental_organization=None)
        else:
            department_q = Q(departmental_organization__in=self.get_departmental())
        if self.query():
            department=self.request.GET.get('department')

            if department!='-':
                instituion=Institutions.objects.filter(departmental_organization=department,short_title__icontains=self.query()[0])
            elif int(self.query()[1])==1:
                instituion=Institutions.objects.filter(department_q,short_title__icontains=self.query()[0])
            else:
                instituion=Institutions.objects.filter(department_q,short_title__icontains=self.query()[0],is_active=True)
        else:
            instituion=Institutions.objects.filter(department_q, is_active=True)
        return instituion
    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Реестр ОО'
        context['institutions'] = self.get_institution()
        context['departmentals']=self.get_departmental()
        department=self.request.GET.get('department')
        if department!='-' and department:
            context['department'] = int(department)
        else:
            context['department'] = 0
        context['types']=self.get_types()
        if self.query():
            context['short_title']=self.query()[0]

        if self.query():
            if int(self.query()[1])==1:
                context['ban']=True
        else:
            context['ban']=False
        return context

    def get_success_url(self):
        return reverse('InstitutionCreate')

    def get_success_message(self, cleaned_data):
        ms = "Логин:" + self.login + "\n" + "Пароль:" + self.password
        success_message = ms
        return success_message % cleaned_data




class BlockInstitution(PermissionRequiredMixin, View):
    permission_required = 'institutions.delete_institutions'
    def get(self,request,institution):

        get_institution=Institutions.objects.get(pk=institution)
        get_institution.is_active=False
        get_institution.save()
        return redirect(request.META.get('HTTP_REFERER'))




class UnblockInstitution(PermissionRequiredMixin, View):
    permission_required = 'institutions.delete_institutions'
    def get(self,request,institution):

        get_institution=Institutions.objects.get(pk=institution)
        get_institution.is_active=True
        get_institution.save()
        return redirect(request.META.get('HTTP_REFERER'))

class EditInstitutuonView(UpdateView):
    template_name='institutions/institutions.html'
    form_class=InstitutionsInfoForm

    def form_valid(self,form):
        return super().form_valid(form)

    def get_object(self,**kwargs):
        return Institutions.objects.get(pk=int(self.kwargs.get('pk')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Редактирование организации'
        return context
    def get_form_kwargs(self):
        kwargs = super(EditInstitutuonView, self).get_form_kwargs()
        kwargs['is_admin'] = self.request.user.is_superuser
        
        return kwargs

    def get_success_url(self):
        return reverse('InstitutionCreate')

#######################################################################

class TranslationOfTheYear(PermissionRequiredMixin, View):

    permission_required='institutions.change_year'
    template_name='institutions/translate_year.html'

    def get(self,request):
        year=Year.objects.get(pk=request.user.institution.year.pk+1)
        context={}
        context['title']='Перевод года'
        context['year']=year
        context['classes']=Classes.objects.filter(
                institution=self.request.user.institution.pk,year=self.request.user.institution.year.pk)
        context['new_classes']=Classes.objects.filter(
                institution=self.request.user.institution.pk,year=self.request.user.institution.year.pk+1)
        context['one_student'] = Student.objects.filter(class_pk__institution=self.request.user.institution, class_pk__institution__year = self.request.user.institution.year, user__is_active= True ).first()
        
        return render(request,self.template_name,context )

    def post(self,request):

        class_pk = int(self.request.POST.get('class_pk'))
        get_old_class = Classes.objects.get(pk=class_pk)
        students = Student.objects.filter(class_pk__pk=class_pk)
        get_new_class = Classes.objects.get(pk=class_pk)
        for student in students:
            student.arсhive_classes.add(get_old_class)
            if self.request.POST.get('new_class_'+str(student.pk)):
                class_student = int(self.request.POST.get('new_class_'+str(student.pk)))
                if class_student!=0:
                    get_new_class = Classes.objects.get(pk=class_student)
                    student.class_pk=get_new_class
                    
            else:
                student.class_pk = None
            
            student.save()
        messages.success(request, 'Учащиеся успешно переведены!')
        return redirect(request.META.get('HTTP_REFERER'))