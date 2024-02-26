from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import News,Category
from .forms import NewsForm,UserRegisterForm,UserLoginForm, MyPasswordResetForm
from django.views.generic import ListView,DetailView,CreateView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import *
from user_account.models import UserNet
from user_account.forms import RegisterForm
from classes.models import Student
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from user_account.tokens import account_activation_token
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from modules.users import confirm_email
from django.contrib.auth.views import LoginView
from institutions.models import Institutions,TypeInstitutions, KindInstitutions, ConnectInstituions



class HomeNews(View):

	template_name = 'news/index.html'
	def get(self,request):
		context = {}
		if request.user.is_authenticated:
			return redirect('HomePageUserAccount')
		return render(request, self.template_name, context)
class GetNewsByCategory(DataMixin,ListView):
	model=News
	template_name='news/index.html'
	context_object_name='news'
	def get_context_data(self,*,object_list=None,**kwargs):
		context=super().get_context_data()
		c_def=self.get_user_context(title='Главная страница')
		return dict(list(context.items())+list(c_def.items()))
	def get_queryset(self):
		return News.objects.filter(category_id=self.kwargs['category_id'],is_published=True)



class View_news(DetailView):
	model=News
	context_object_name='news_item'
	pk_url_kwarg='news_id'
	template_name='news/view_news.html'
class CreateNews(LoginRequiredMixin, CreateView):
	form_class=NewsForm
	template_name='news/add_news.html'
	#success_url='' ----Url редиректа

def register(request):
	context = {}
	context['title'] = 'Регистрация'
	if request.method=="POST":
		
		code = request.POST.get('code')
		user_get = UserNet.objects.filter(code=code).first()
		if user_get:
			return redirect('register2', code=code)
		else:
			context['error'] = True
			context['code'] = code

	return render(request,'news/register.html',context)

def register_user_info(request, code):
	get_user = UserNet.objects.filter(code=code).first()
	context = {}
	context['title'] = 'Регистрация'
	if get_user:
		if request.method=="POST":
			form=UserRegisterForm(request.POST, instance=get_user)
			if form.is_valid():
				user=form.save(commit=False)
				user.registration = True
				user.code = None
				user.save()
				us = UserNet.objects.get(pk=user.pk)
				confirm_email(us,request)
				login(request, get_user)
				messages.success(request,'Вы успешно зарегистрировались')
				return redirect('HomePageUserAccount')
			else:
				messages.error(request,'Ошибка регистрации')
				context['error'] = True
		else:
			form=UserRegisterForm(instance=get_user)
		return render(request,'news/register2.html',{"form":form})




class MyLoginView(LoginView):

    redirect_authenticated_user = True
    template_name = 'news/login.html'
    def get_success_url(self):
        return reverse_lazy('HomePageUserAccount') 
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))



def user_logout(request):
	logout(request)
	return redirect('login')


def admin_panel(request):
	templ = 'news/admin-panel.html'
	return render(request,templ)

def student_code(request):
	
	chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

	students = Student.objects.all()
	chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
	

	for i in students:
		code = ''
		for k in range(8):
			code += random.choice(chars)
			
		i.user.code = code
		i.user.save()
	

	return redirect('AdminPanel')



'''
def add_news(request):
	if request.method=='POST':
		form=NewsForm(request.POST)
		if form.is_valid():
			#print(form.cleaned_data)
			#news=News.objects.create(**form.cleaned_data)
			news=form.save()
			return redirect(news)
	else:
		form=NewsForm()
	return render(request,'news/add_news.html',{"form":form},)
'''


class UserForgotPasswordForm(PasswordResetView):
    """
    Запрос на восстановление пароля
    """
    form_class = MyPasswordResetForm
    template_name = 'news/password_reset.html'

class Connection(View):
	def get(self,request):
		context = {}
		context['types'] = TypeInstitutions.objects.all()
		context['kinds'] = KindInstitutions.objects.all()
		context['departments'] = Institutions.objects.filter(
                typeInstitutions__title="Орган управления", is_active=True
            )
		template = 'news/connection.html'
		return render(request,template,context)
	def post(self,request):
		data = [
			request.POST.get('iname'),
			request.POST.get('sname'),
			request.POST.get('type'),
			request.POST.get('kind'),
			request.POST.get('city'),
			request.POST.get('department'),
			request.POST.get('name'),
			request.POST.get('surname'),
			request.POST.get('mname'),
			request.POST.get('dr'),
			request.POST.get('number'),
			request.POST.get('message'),
			request.POST.get('email')

		]
		kind = KindInstitutions.objects.get(pk=int(data[3]))
		type_ = TypeInstitutions.objects.get(pk=int(data[2]))
		if data[5]!='Не выбрано':
			institution = Institutions.objects.get(pk=int(data[5]))
		else:
			institution = Institutions.objects.get(title="Организации ПК Бусел")

		if data[0] and data[1] and data[4] and data[6] and data[7] and data[8] and data[10] and data[12]:
			ConnectInstituions.objects.create(title=data[0],short_title=data[1],typeInstitutions=type_,kindInstitutions=kind,city=data[4], institution=institution, name=data[6],surname=data[7], middle_name=data[8],birthday=data[9],phone=data[10],comment=data[11], email=data[12])
			messages.success(request,'Заявка принята')
		else:
			messages.error(request,'Ошибка')
		return redirect('Connection')