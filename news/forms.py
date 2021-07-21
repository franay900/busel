from django import forms
from .models import News
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from user_account.models import UserNet


class UserLoginForm(AuthenticationForm):
	username=forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-control'}))
	password=forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-control'}))
	
class UserRegisterForm(UserCreationForm):
	email=forms.EmailField(label='Почта',widget=forms.EmailInput(attrs={'class':'form-control'}))
	username=forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-control'}))
	password1=forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2=forms.CharField(label='Пароль еще раз',widget=forms.PasswordInput(attrs={'class':'form-control'}))
	class Meta:
		model=UserNet
		fields=('username','email')
class NewsForm(forms.ModelForm):
	class Meta:
		model=News
		#fields='__all__' --- Все значения
		fields=['title','content','is_published','category']
		widgets={
			'title':forms.TextInput(attrs={'class':'form-control'}),
			'content':forms.Textarea(attrs={'class':'form-control'}),
			'category':forms.Select(attrs={'class':'form-control'}),

		}

	### Без моделей
	''' 
	class NewsForm(forms.Form):
		title=forms.CharField(max_length=150,label='Заголовок',widget=forms.TextInput(attrs={"class":"form-control"}))
		content=forms.CharField(label='Текст',widget=forms.Textarea(attrs={"class":"form-control"}))
		is_published=forms.BooleanField(label='Опубликовано?',initial=True)
		category=forms.ModelChoiceField(queryset=Category.objects.all(),label='Категория',empty_label='Выберите категорию',widget=forms.Select(
			attrs={
			"class":"custom-select",
			"rows":1,

			}))
	'''
	