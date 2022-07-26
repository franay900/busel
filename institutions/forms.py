from django import forms
from .models import *
from user_account.models import *
from journal.models import LessonType, TypeExams
from news.models import AdsInstitution

class InstitutionsInfoForm(forms.ModelForm):
	error_css_class = 'is-invalid'
	class Meta:
		model=Institutions
		fields=['title','short_title','system_mark','year','typeInstitutions','kindInstitutions','departmental_organization', 'photo']
	def __init__(self,*args,**kwargs):
		if 'is_admin' in kwargs:
			is_admin = kwargs.pop('is_admin')
		else:
			is_admin = False
		super().__init__(*args,**kwargs)
		if not is_admin:
			self.fields['departmental_organization'].disabled = True
			self.fields['typeInstitutions'].disabled = True
		for field in self.fields:
			if field != 'system_mark' and field != 'typeInstitutions' and field != 'kindInstitutions' and field != 'year' and field != 'departmental_organization':
				self.fields[field].widget.attrs['class']='form-control'
			else:
				self.fields[field].widget.attrs['class']='custom-select'


class TypeLessonForm(forms.ModelForm):

	class Meta:
		model=LessonType
		fields=['name','short_name']

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['name'].widget.attrs['class']='form-control'
		self.fields['short_name'].widget.attrs['class']='form-control'

class TypeExamsForm(forms.ModelForm):

	class Meta:
		model=TypeExams
		fields=['name','short_name']

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['name'].widget.attrs['class']='form-control'
		self.fields['short_name'].widget.attrs['class']='form-control'



class PeriodsForm(forms.ModelForm):
	class Meta:
		model=PeriodProfile
		fields=['title']
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['title'].widget.attrs['class']='form-control'

class BellForm(forms.ModelForm):
	class Meta:
		model=BellProfile
		fields=['title']
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['title'].widget.attrs['class']='form-control'


class SubjectForm(forms.ModelForm):
	class Meta:
		model=Subject
		fields=['title','short_title']
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class']='form-control'

class InstitutionForm(forms.ModelForm):
	class Meta:
		model=Institutions
		fields=['title','short_title','year','typeInstitutions']
	def __init__(self,*args,**kwargs):
		types=kwargs.pop('types')
		super().__init__(*args,**kwargs)
		self.fields['typeInstitutions'].queryset=TypeInstitutions.objects.filter(pk__in=types)
		for field in self.fields:
			self.fields[field].widget.attrs['class']='form-control'



class AdsForm(forms.ModelForm):

	class Meta:
		model=AdsInstitution
		fields=['title', 'text']
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class']='form-control'

class InstitutionEditForm(forms.ModelForm):

	error_css_class = 'is-invalid'
	class Meta:
		model=Institutions
		fields=['title','short_title','system_mark','year','typeInstitutions','kindInstitutions','departmental_organization', 'photo']
	def __init__(self, *args,**kwargs):
		
		is_admin = kwargs.pop('is_admin')
		super().__init__(*args,**kwargs)
		
		for field in self.fields:
			if field != 'system_mark' and field != 'typeInstitutions' and field != 'kindInstitutions' and field != 'year' and field != 'departmental_organization':
				self.fields[field].widget.attrs['class']='form-control'
			else:
				self.fields[field].widget.attrs['class']='custom-select'

		