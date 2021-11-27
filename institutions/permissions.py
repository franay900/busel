from user_account.permissions import AdminPermissionMixin
from classes.models import PeriodProfile
from django.http import HttpResponseForbidden
class InstitutionsMixin(AdminPermissionMixin):

	def has_permissions(self,**kwargs):
		try:
			return self.get_object().institution==self.request.user.institution
		except:
			return HttpResponseForbidden()
		
