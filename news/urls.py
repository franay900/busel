from django.urls import path
from .views import *

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
urlpatterns = [
	path('',HomeNews.as_view(),name='home'),
	path('category/<int:category_id>',GetNewsByCategory.as_view(),name='category'),
	path('view_news/<int:news_id>/',View_news.as_view(),name="view_news"),
	path('add_news/',CreateNews.as_view(),name="add_news"),
	path('register/step1',register,name='register'),
	path('register/step2/<str:code>',register_user_info,name='register2'),

	path('user_login',MyLoginView.as_view(),name='login'),
	path('user_logout',user_logout,name='logout'),
	path('admin-panel', admin_panel, name='AdminPanel'),
	path('student-codes/create', student_code,name='CreateStudentsCode'),

	path('connection/', Connection.as_view(),name='Connection'),

	#Смена пароля
	path('password-reset/', UserForgotPasswordForm.as_view(),name='password-reset'),
	path('password-reset/done/', PasswordResetDoneView.as_view(template_name='news/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='news/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='news/password_reset_complete.html'),name='password_reset_complete'),

]