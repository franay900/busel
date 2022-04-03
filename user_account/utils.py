from .models import UserNet
from institutions.models import TypeInstitutions
class UserMixin:
	def getUserByInstitutions(self,**kwargs):
		context=kwargs
		institutions=self.request.user.institution
		if self.request.user.is_superuser:
			users=UserNet.objects.all()
		else:
			type_inst=institutions.typeInstitutions.pk
			groups=TypeInstitutions.objects.filter(pk=type_inst).values('group')
			groupsUser=[]
			for i in groups:
				groupsUser.append(i['group'])
			users=UserNet.objects.filter(institution=institutions,groups__pk__in=groupsUser,is_active=True).distinct()

		context['users']=users
		return context


