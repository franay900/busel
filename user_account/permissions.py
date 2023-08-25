from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from user_account.models import UserNet
from django.shortcuts import redirect
from django.contrib.auth import logout



class AdminPermissionMixin:
	def has_permissions(self):
		user_pk=self.request.user.pk
		try:
			user=UserNet.objects.get(pk=user_pk,groups__name__in=['Администратор ОО','Завуч','Администратор ПОО'])
			return user.groups
		except:
			pass
		if self.request.user.is_superuser:
			return True

	def dispatch(self,request,*args,**kwargs):
		if not self.has_permissions():
			return HttpResponseForbidden()
		return super().dispatch(request,*args,**kwargs)




class RegisterMixin():
	def has_permissions(self):
		if self.request.user.is_superuser or self.request.user.institution.is_active==True:
			
			return True
	def dispatch(self,request,*args,**kwargs):
		if not self.has_permissions():
			logout(request)
			return redirect('login')
		return super().dispatch(request,*args,**kwargs)