from django import forms 
from .models import KTP,Sections_KTP


class KTPForm(forms.ModelForm):
	
	class Meta:
		model = KTP
		fields = ['name', 'class_number', 'subject_ktp']

	def __init__(self, *args, **kwargs):
		super().__init__(*args,**kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

class SectionsKTPForm(forms.ModelForm):

	class Meta:
		model = Sections_KTP
		fields = ['name']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'
