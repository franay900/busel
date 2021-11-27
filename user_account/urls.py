from django.urls import path
from .views import*


urlpatterns= [
	path('',HomePageAccountView.as_view(),name='HomePageUserAccount'),
	path('users',UsersView.as_view(),name='users'),
	path('user_edit/<int:user_id>/',user_edit_view,name='user_edit'),
	path('registration/',Registration.as_view(),name='Registration'),
	path('user_add/',AddUser.as_view(),name='AddUser'),
	path('user_ban/<int:user_id>/',BanUser.as_view(),name='BanUser'),
	path('import/',ImportUsers.as_view(),name='ImportUser'),
	
]
