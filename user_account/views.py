import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from .forms import UserEditForm,RegisterForm,SetPassword
from .permissions import AdminPermissionMixin,RegisterMixin
from user_account.models import UserNet,FileTemplates
from .utils import *
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from institutions.permissions import InstitutionsMixin
from modules.users import get_user, generate_login
from django.contrib import messages
from django.http import HttpResponseForbidden,HttpResponseRedirect


class HomePageAccountView(RegisterMixin,LoginRequiredMixin, ListView):
    model = UserNet
    login_url = 'login'
    queryset = UserNet.objects.all()
    template_name = 'user_account/index.html'


class UsersView(PermissionRequiredMixin,UserMixin, ListView):
    model = UserNet
    template_name = 'user_account/users.html'
    permission_required = 'user_account.view_usernet'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        c_def = self.getUserByInstitutions(title='Сотрудники')
        return dict(list(context.items()) + list(c_def.items()))


def user_edit_view(request,user_id):
    user=UserNet.objects.get(pk=user_id)
    if user.institution== request.user.institution:
        password_form=SetPassword(user=user)
        form=UserEditForm(instance=user,user=user.institution.typeInstitutions)
        if request.method=="POST":
            save_form=UserEditForm(request.POST,request.FILES or None,instance=user,user=user.institution.typeInstitutions)
            if save_form.is_valid():
                form=save_form
                user=form.save()
                messages.success(request,'Информация обновлена')

            save_password=SetPassword(data=request.POST,user=user)
            if save_password.is_valid():
                save_password.save()
                messages.success(request,"Пароль успешно обновлен")

            
        context={"form":form,'password_form':password_form,'title':'Редактирование пользователя'}
        return render(request,'user_account/user_update.html',context)
    else:
        return HttpResponseForbidden()
class UserEditView(PermissionRequiredMixin,SuccessMessageMixin,InstitutionsMixin,UpdateView):
    model = UserNet
    form_class = UserEditForm
    template_name = 'classes/user_update.html'
    pk_url_kwarg = 'user_id'
    success_message = 'Информация обновлена'
    error_message='Ошибка'
    permission_required = 'user_account.change_usernet'
    login_url='login'
    def get_form_kwargs(self):
        kwargs = super(UserEditView, self).get_form_kwargs()
        kwargs['user'] =kwargs['instance'].institution.typeInstitutions
        return kwargs
    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Личная карточка пользователя'
        return context

class Registration(UpdateView):
    form_class = RegisterForm
    template_name = 'user_account/user_update.html'
    def get_object(self,**kwargs):
        return UserNet.objects.get(pk=self.request.user.pk)
    def form_valid(self, form):
        user = form.save(commit=False)
        user.registration=True
        user.set_password(self.request.POST.get("password"))
        user.save()
        return super().form_valid(form)
    def get_success_url(self): 
        return reverse('login')


class AddUser(AdminPermissionMixin, SuccessMessageMixin, CreateView):
    form_class = UserEditForm
    template_name = 'user_account/user_update.html'
    def get_form_kwargs(self):
        kwargs = super(AddUser, self).get_form_kwargs()
        kwargs['user'] =self.request.user.institution.typeInstitutions
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
        user = form.save(commit=False)
        user.set_password(self.password)
        user.username=self.login
        user.institution_id = self.request.user.institution.pk
        user.save()
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Добавление пользователя'
        return context

    def get_success_url(self):
        return reverse('users')
    def get_success_message(self, cleaned_data):
        ms = "Логин:" + self.login + "\n" + "Пароль:" + self.password
        success_message = ms
        return success_message % cleaned_data

class BanUser(View):
    
    def get(self, request, user_id):
        user_get=UserNet.objects.get(pk=user_id)
        user_get.is_active=False
        user_get.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ImportUsers(View):
    def get(self,request):
        context={}
        context['title']='Импорт пользователей'
        context['file']=FileTemplates.objects.filter(name='Шаблон для импорта пользователей').first()
        return render(request,'user_account/import_user.html',context)
    def post(self,request):
        context={}

        if 'add' in request.POST:
            get_users=request.POST.getlist("users")
            for user in get_users:
                user_get=UserNet.objects.get(pk=user)
                user_get.is_active=True
                user_get.save()
            messages.success(request, 'Пользователи успешно импортированы!')
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
                login=generate_login()[0]
                password=generate_login()[1]
                if first_name and last_name and patronymic and gender and birth_day:
                    user_pk=UserNet.objects.create_user(is_active=False,username=login,password=password,last_name=last_name,first_name=first_name,middle_name=patronymic,gender=gender,birth_day=birth_day,institution=self.request.user.institution)
                    user_pk.groups.set([2])
                    arr.append([last_name,first_name,patronymic,gender,birth_day,login,password,user_pk.pk])
                    

        context['title']='Результат импорта'
        context['users']=arr
        return render(request,'user_account/import_result.html',context)