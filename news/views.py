from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import News,Category
from .forms import NewsForm,UserRegisterForm,UserLoginForm
from django.views.generic import ListView,DetailView,CreateView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import *
from user_account.models import UserNet
from user_account.forms import RegisterForm

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
			print(1)
			form=UserRegisterForm(request.POST, instance=get_user)
			if form.is_valid():
				user=form.save(commit=False)
				user.registration = True
				user.code = None
				user.save()
				login(request, get_user)
				messages.success(request,'Вы успешно зарегистрировались')
				return redirect('HomePageUserAccount')
			else:
				messages.error(request,'Ошибка регистрации')
				context['error'] = True
		else:
			form=UserRegisterForm(instance=get_user)
		return render(request,'news/register2.html',{"form":form})



def user_login(request):
	context={}
	if request.method=='POST':
		form=UserLoginForm(data=request.POST)

		if form.is_valid():
			
			user=form.get_user()
			if user.is_superuser:
				login(request, user)
				return redirect('HomePageUserAccount')
			elif user.institution.is_active:
				login(request, user)
				return redirect('HomePageUserAccount')
			else:
				messages.warning(request, "Ваша организация заблокирована!")
				
		else:
			messages.warning(request, "Неверный логин или пароль!")
			context['login'] = form.cleaned_data.get("username")
			context['error']=True
	else:
		form=UserLoginForm()
	context['form']=form
	return render(request,'news/login.html',context)

def user_logout(request):
	logout(request)
	return redirect('login')
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
