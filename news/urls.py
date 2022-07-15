from django.urls import path
from .views import *
urlpatterns = [
	path('',HomeNews.as_view(),name='home'),
	path('category/<int:category_id>',GetNewsByCategory.as_view(),name='category'),
	path('view_news/<int:news_id>/',View_news.as_view(),name="view_news"),
	path('add_news/',CreateNews.as_view(),name="add_news"),
	path('register/step1',register,name='register'),
	path('register/step2/<str:code>',register_user_info,name='register2'),

	path('user_login',user_login,name='login'),
	path('user_logout',user_logout,name='logout')

]