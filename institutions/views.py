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
from journal.models import LessonType, TypeExams
from classes.models import Classes, Student, Professions, Сurriculum, Floors


class InstitutionsHomeView(PermissionRequiredMixin, SuccessMessageMixin, View):
    model = Institutions
    form_class = InstitutionsInfoForm
    second_form_class = TypeLessonForm
    form_class_3 = TypeExamsForm
    template_name = "institutions/institutions.html"
    success_message = "Информация об организации успешно обновлена!"
    permission_required = "institutions.view_institutions"

    def get(self, request, **kwargs):
        context = {}
        context["title"] = "Настройки организации"
        context["types"] = LessonType.objects.filter(
            Q(institution=request.user.institution) | Q(institution=None)
        )
        context["typese"] = TypeExams.objects.filter(
            Q(institution=request.user.institution) | Q(institution=None)
        )
        if "form" not in context:
            context["form"] = self.form_class(instance=self.get_object(), is_admin=self.request.user)

        if "form2" not in context:
            context["form2"] = self.second_form_class()
        if "form3" not in context:
            context["form3"] = self.form_class_3()
        context['institution'] = self.request.user.institution
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        if "title" in request.POST:
            form = self.form_class(
                request.POST, request.FILES or None, instance=self.get_object(), is_admin=self.request.user
            )
            if form.is_valid():
                form.save()

        if "typelesson" in request.POST:
            form2 = self.second_form_class(request.POST)
            if form2.is_valid():
                form2.instance.institution = request.user.institution
                form2.save()

        if "exams" in request.POST:
            form3 = self.form_class_3(request.POST)
            if form3.is_valid():
                form3.instance.institution = request.user.institution
                form3.save()

        return redirect(request.META.get("HTTP_REFERER"))

    def get_object(self, **kwargs):
        return Institutions.objects.get(pk=self.request.user.institution.pk)


class AdsCreateView(CreateView):
    form_class = AdsForm
    template_name = "institutions/ads.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["title"] = "Объявления"
        context["ads"] = AdsInstitution.objects.filter(
            institution=self.request.user.institution
        )
        return context

    def form_valid(self, form):
        form.instance.institution_id = self.request.user.institution.pk
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("create_ad")


class AdsDeleteView(View):
    def get(self, request, *args, **kwargs):
        id_ = self.kwargs.get("pk")
        AdsInstitution.objects.get(pk=id_).delete()
        return redirect(request.META.get("HTTP_REFERER"))


class StudyPeriodsView(PermissionRequiredMixin, ListView):
    model = PeriodProfile
    template_name = "institutions/study_periods.html"
    permission_required = "institutions.view_periodprofile"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        period_profile = PeriodProfile.objects.filter(
            institution=self.request.user.institution.pk,
            year=self.request.user.institution.year.pk,
        )
        context["period_profile"] = period_profile
        context["title"] = "Профили учебных периодов"
        return context


class Add_periods(AdminPermissionMixin, CreateView):
    form_class = PeriodsForm
    template_name = "institutions/add_periods.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["title"] = "Добавление учебного периода"
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
        one_period = Periods.objects.create(
            profile=profile_pk, start=one_start, end=one_end
        )
        two_start = self.request.POST.get("two_start")
        two_end = self.request.POST.get("two_end")
        two_period = Periods.objects.create(
            profile=profile_pk, start=two_start, end=two_end
        )

        if int(type_period) == 3 or int(type_period) == 4:
            three_start = self.request.POST.get("three_start")
            three_end = self.request.POST.get("three_end")
            three_period = Periods.objects.create(
                profile=profile_pk, start=three_start, end=three_end
            )
        if int(type_period) == 4:
            four_start = self.request.POST.get("four_start")
            four_end = self.request.POST.get("four_end")
            four_period = Periods.objects.create(
                profile=profile_pk, start=four_start, end=four_end
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("StudyPeriods")


class DeleteProfilePeriods(PermissionRequiredMixin, View):
    permission_required = "institutions.view_periodprofile"

    def get(self, request, pk):
        PeriodProfile.objects.get(pk=pk).delete()
        return redirect("StudyPeriods")


class StudyPeriodsUpdateView(View, Study_Periods):
    template_name = "institutions/study_periods_edit.html"

    def get(self, request, profile_pk):
        context = {}
        context["title"] = "Редактирование учебных периодов"
        context["periods"] = self.get_periods()
        context["period_profile"] = self.get_period_profile()
        return render(request, self.template_name, context)

    def post(self, request, profile_pk):
        self.get_update_period()

        return redirect("StudyPeriods")


# Звонки
class BellProfileView(PermissionRequiredMixin, ListView):
    model = BellProfile
    template_name = "institutions/bell_profile.html"
    permission_required = 'institutions.view_belltimetable'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["title"] = "Профили звонков"
        context["bell_profiles"] = BellProfile.objects.filter(
            institution=self.request.user.institution.pk
        )
        return context


class BellProfileCreateView(AdminPermissionMixin, CreateView):
    form_class = BellForm
    template_name = "institutions/bell_profile_create.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["title"] = "Добавление профиля звонков периода"
        context["days"] = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
        ]
        context['numbers'] = list(range(1,self.request.user.institution.number_of_lessons+1))
        context['number'] = self.request.user.institution.number_of_lessons
        return context

    def form_valid(self, form):
        bell_profile = form.save(commit=False)
        form.instance.institution_id = self.request.user.institution.pk
        bell_profile.save()
        profile = bell_profile
        n = self.request.user.institution.number_of_lessons
        a = 0
        while a <= 5:
            a += 1
            for i in range(n):
                i += 1
                bell_start = self.request.POST.get("b" + str(a) + str(i))
                bell_end = self.request.POST.get("e" + str(a) + str(i))
                if bell_start and bell_end:
                    bell_period = BellTimetable.objects.create(
                        profile=bell_profile,
                        start=bell_start,
                        end=bell_end,
                        day=a,
                        lesson=i,
                    )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("Bell_profile_list")




class SubjectView(PermissionRequiredMixin, CreateView):
    form_class = SubjectForm
    template_name = "institutions/subject_list.html"
    permission_required = "institutions.view_subject"
    def form_valid(self, form):
        form.instance.institution_id = self.request.user.institution.pk
        if (
            self.request.user.institution.typeInstitutions.title
            == "Профессиональная образовательная организация"
        ):
            t_get = TypeInstitutions.objects.get(
                title="Профессиональная образовательная организация"
            )
            form.instance.type_org = t_get
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()

        if (
            self.request.user.institution.typeInstitutions.title
            == "Профессиональная образовательная организация"
        ):
            context["subjects"] = Subject.objects.filter(
                Q(institution=self.request.user.institution.pk) | Q(institution=None),
                type_org__title="Профессиональная образовательная организация",
            ).order_by("title")
            context["title"] = "Учебные дисциплины"
        else:
            context["subjects"] = Subject.objects.filter(
                Q(institution=self.request.user.institution.pk) | Q(institution=None)
            ).order_by("title")
            context["title"] = "Учебные предметы"
        context["institution"] = self.request.user.institution
        return context

    def get_success_url(self):
        return reverse("Subject_list")


class DeleteSubject(InstitutionsMixin, DeleteView):
    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Subject, id=id_)

    def get(self, request, pk):
        Subject.objects.get(pk=pk).delete()
        return redirect("Subject_list")


class ProfessionsView(AdminPermissionMixin, CreateView):
    form_class = ProfessionsForm
    template_name = "institutions/professions.html"

    def form_valid(self, form):
        form.instance.institution_id = self.request.user.institution.pk

        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()

        context["subjects"] = Professions.objects.filter(
            Q(institution=self.request.user.institution.pk) | Q(institution=None)
        ).order_by("name")
        context["title"] = "Профессии/специальности"

        context["institution"] = self.request.user.institution
        return context

    def get_success_url(self):
        return reverse("ProfessionList")


class DeleteProfession(InstitutionsMixin, DeleteView):
    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Professions, id=id_)

    def get(self, request, pk):
        Professions.objects.get(pk=pk).delete()
        return redirect("ProfessionList")


# Админка ###############################################################################
class InstitutionCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = InstitutionForm
    template_name = "institutions/institutions_create.html"
    permission_required = "institutions.add_institutions"

    def get_types(self):
        if self.request.user.is_superuser:
            types = TypeInstitutions.objects.all()
        elif self.request.user.institution.typeInstitutions.title == "Орган управления":
            types = TypeInstitutions.objects.filter(title__in=["Общеобразовательная организация", "Профессиональная образовательная организация"])
        return types

    def get_departmental(self):
        if self.request.user.is_superuser == True:
            departmentals = Institutions.objects.filter(
                typeInstitutions__title="Орган управления", is_active=True
            )
        else:
            departmentals = Institutions.objects.filter(
                typeInstitutions__title="Орган управления",
                pk=self.request.user.institution.pk,
                is_active=True,
            )
        return departmentals

    def get_form_kwargs(self):
        kwargs = super(InstitutionCreate, self).get_form_kwargs()
        kwargs["types"] = self.get_types().values_list("pk")
        return kwargs

    def form_valid(self, form):
        chars = "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        self.login = ""
        self.password = ""

        institutions_create = form.save(commit=True)
        if self.request.user.is_superuser == False:
            institutions_create.departmental_organization = (
                self.request.user.institution
            )
            department_institution = Institutions.objects.get(
                pk=self.request.user.institution.pk
            )
            lim = department_institution.lim - 1
            department_institution.save()
        institutions_create.save()
        for i in range(8):
            self.login += random.choice(chars)

        group = TypeInstitutions.objects.get(
            pk=self.request.POST.get("typeInstitutions")
        ).group.all()[0]
        user = UserNet.objects.create_user(
            username=self.login, code=self.login, institution=institutions_create
        )
        user.groups.set([group])
        return super().form_valid(form)

    def query(self):
        short_title = self.request.GET.get("short_title")
        ban = self.request.GET.get("ban")
        if (short_title or ban) is not None:
            return short_title, ban

    def get_institution(self):
        if self.request.user.is_superuser == True:
            department_q = Q(departmental_organization__in=self.get_departmental()) | Q(
                departmental_organization=None
            )
        else:
            department_q = Q(departmental_organization__in=self.get_departmental())
        if self.query():
            department = self.request.GET.get("department")

            if department != "-":
                instituion = Institutions.objects.filter(
                    departmental_organization=department,
                    short_title__icontains=self.query()[0],
                )
            elif int(self.query()[1]) == 1:
                instituion = Institutions.objects.filter(
                    department_q, short_title__icontains=self.query()[0]
                )
            else:
                instituion = Institutions.objects.filter(
                    department_q, short_title__icontains=self.query()[0], is_active=True
                )
        else:
            instituion = Institutions.objects.filter(department_q, is_active=True)
        return instituion

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Реестр ОО"
        context["institutions"] = self.get_institution()
        context["departmentals"] = self.get_departmental()
        department = self.request.GET.get("department")
        if department != "-" and department:
            context["department"] = int(department)
        else:
            context["department"] = 0
        context["types"] = self.get_types()
        if self.request.user.is_superuser:

            context['uo'] = False
        else:
            context['uo'] = True
        if self.query():
            context["short_title"] = self.query()[0]

        if self.query():
            if int(self.query()[1]) == 1:
                context["ban"] = True
        else:
            context["ban"] = False
        return context

    def get_success_url(self):
        return reverse("InstitutionCreate")

    def get_success_message(self, cleaned_data):
        ms = "Пригласительный код:" + self.login
        success_message = ms
        return success_message % cleaned_data


class BlockInstitution(PermissionRequiredMixin, View):
    permission_required = "institutions.delete_institutions"

    def get(self, request, institution):
        get_institution = Institutions.objects.get(pk=institution)
        get_institution.is_active = False
        get_institution.save()
        return redirect(request.META.get("HTTP_REFERER"))


class UnblockInstitution(PermissionRequiredMixin, View):
    permission_required = "institutions.delete_institutions"

    def get(self, request, institution):
        get_institution = Institutions.objects.get(pk=institution)
        get_institution.is_active = True
        get_institution.save()
        return redirect(request.META.get("HTTP_REFERER"))


class DeleteInstitutionForever(PermissionRequiredMixin, View):
    permission_required = "institutions.delete_institutions"

    def get(self,request, institution):
        get_institution = Institutions.objects.get(pk=institution)
        title = get_institution.short_title
        AdsInstitution.objects.filter(institution=get_institution).delete()
        BellProfile.objects.filter(institution=get_institution).delete()
        PeriodProfile.objects.filter(institution=get_institution).delete()
        Classes.objects.filter(institution=get_institution).delete()
        Сurriculum.objects.filter(institution=get_institution).delete()
        LessonType.objects.filter(institution=get_institution).delete()
        TypeExams.objects.filter(institution=get_institution).delete()
        get_institution.delete()
        messages.success(request,f'Организация {title} удалена навсегда')
        return redirect(request.META.get("HTTP_REFERER"))


class ConnectionRequests(PermissionRequiredMixin, View):
    permission_required = "institutions.change_institutions"

    def get(self, request):
        context = {}
        context['title'] = 'Заявки на подключение'
        if request.user.is_superuser:
            context['requests'] = ConnectInstituions.objects.all()
        else:
            context['requests'] = ConnectInstituions.objects.filter(institution=request.user.institution)
        return render(request, 'institutions/request.html',context)

class DeleteConnection(PermissionRequiredMixin, View):
    permission_required = "institutions.delete_institutions"
    def get(self, request,pk):
        ConnectInstituions.objects.get(pk=pk).delete()
        messages.error(request,'Заявка успешно отклонена!')
        return redirect('ConnectionRequests')

class ApprovalConnection(PermissionRequiredMixin, View):
    permission_required = "institutions.change_institutions"
    def get(self, request,pk):
        connection = ConnectInstituions.objects.get(pk=pk)
        login = ''
        chars = "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        for i in range(8):
            login += random.choice(chars)
        institutions_create = Institutions.objects.create(title=connection.title, short_title=connection.short_title,year=Year.objects.all().last(),
                                                          typeInstitutions=connection.typeInstitutions,kindInstitutions=connection.kindInstitutions,
                                                          departmental_organization=connection.institution, inn=connection.inn)


        group = connection.typeInstitutions.group.all()[0]
        user = UserNet.objects.create_user(first_name=connection.name, last_name=connection.surname, middle_name=connection.middle_name,
            username=login, code=login, institution=institutions_create
        )
        user.groups.set([group])
        ConnectInstituions.objects.get(pk=pk).delete()
        messages.success(request,f'Заявка успешно одобрена! Пригласительный код:{login}')
        return redirect('ConnectionRequests')


class EditInstitutuonView(UpdateView):
    template_name = "institutions/institutions.html"
    form_class = InstitutionsInfoForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_object(self, **kwargs):
        return Institutions.objects.get(pk=int(self.kwargs.get("pk")))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["title"] = "Редактирование организации"
        context['institution'] = self.get_object()
        return context

    def get_form_kwargs(self):
        kwargs = super(EditInstitutuonView, self).get_form_kwargs()
        kwargs["is_admin"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("InstitutionCreate")


#######################################################################


class TranslationOfTheYear(PermissionRequiredMixin, View):
    permission_required = "institutions.change_year"
    template_name = "institutions/translate_year.html"

    def get(self, request):
        year = Year.objects.get(pk=request.user.institution.year.pk + 1)
        context = {}
        context["title"] = "Перевод года"
        context["year"] = year
        context["classes"] = Classes.objects.filter(
            institution=self.request.user.institution.pk,
            year=self.request.user.institution.year.pk,
        )
        context["new_classes"] = Classes.objects.filter(
            institution=self.request.user.institution.pk,
            year=self.request.user.institution.year.pk + 1,
        )
        context["one_student"] = Student.objects.filter(
            class_pk__institution=self.request.user.institution,
            class_pk__institution__year=self.request.user.institution.year,
            user__is_active=True,
        ).first()

        return render(request, self.template_name, context)

    def post(self, request):
        class_pk = int(self.request.POST.get("class_pk"))
        get_old_class = Classes.objects.get(pk=class_pk)
        students = Student.objects.filter(class_pk__pk=class_pk)
        get_new_class = Classes.objects.get(pk=class_pk)
        for student in students:
            student.old_classes.add(get_old_class)
            if self.request.POST.get("new_class_" + str(student.pk)):
                class_student = int(
                    self.request.POST.get("new_class_" + str(student.pk))
                )
                if class_student != 0:
                    get_new_class = Classes.objects.get(pk=class_student)
                    student.class_pk = get_new_class

            else:
                student.class_pk = None

            student.save()
        messages.success(request, "Учащиеся успешно переведены!")
        return redirect(request.META.get("HTTP_REFERER"))