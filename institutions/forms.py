from django import forms
from .models import *
from user_account.models import *
class InstitutionsInfoForm(forms.ModelForm):
	error_css_class = 'is-invalid'
	class Meta:
		model=Institutions
		fields=['title','short_title','system_mark','year', 'photo']
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class']='form-control'


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
		super().__init__(*args,**kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class']='form-control'

