from django import forms
from .models import *
from user_account.models import *
from django.db.models import Q
class СurriculumForm(forms.ModelForm):
	class Meta:
		model=Сurriculum
		fields=['title']
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class']='form-control'
class ClassForm(forms.ModelForm):

	class Meta:
		model=Classes
		fields=['class_number','letter','сurriculum','bell_profile','period_profile','class_teacher']
	def __init__(self,*args,**kwargs):
		if 'edit' in kwargs:
			self.edit=kwargs.pop('edit')
		else:
			self.edit=False
		self.teacher=kwargs.pop('teacher')
		super().__init__(*args,**kwargs)
		self.fields['class_teacher'].queryset = UserNet.objects.filter(institution=self.teacher.pk,groups=2,is_active=True).distinct()
		self.fields['сurriculum'].queryset = Сurriculum.objects.filter(institution=self.teacher.pk,year=self.teacher.year.pk)
		self.fields['bell_profile'].queryset = BellProfile.objects.filter(institution=self.teacher.pk)
		self.fields['period_profile'].queryset = PeriodProfile.objects.filter(institution=self.teacher.pk,year=self.teacher.year.pk)
		for field in self.fields:
			self.fields[field].widget.attrs['class']='form-control'
		if self.edit==False:
			self.fields['class_number'].disabled=True
	
class SubgroupsForm(forms.ModelForm):
	class Meta:
		model=Subgroups
		fields=['name','subject_pk','subject_pk']

	def __init__(self,*args,**kwargs):
		self.class_number2=kwargs.pop('class_number')
		super().__init__(*args,**kwargs)
		self.fields['subject_pk'].queryset = СurriculumSubject.objects.filter(class_number=self.class_number2)
		for field in self.fields:
			self.fields[field].widget.attrs['class']='form-control'
class StudentForm(forms.ModelForm):
    
    class Meta:

        model = UserNet
        CHOICES =(
            ("мужской", "мужской"),
            ("женский", "женский"),
 
        )
        fields=['last_name','first_name','middle_name','avatar','email','birth_day','gender']
        avatar = forms.ImageField()
        widgets={
	    	'last_name':forms.TextInput(attrs={'class':'form-control'}),
	    	'birth_day':forms.DateInput(attrs={'class':'form-control','type': 'date'}),
	    	'first_name':forms.TextInput(attrs={'class':'form-control'}),
	    	'middle_name':forms.TextInput(attrs={'class':'form-control'}),
	    	'birth_day':forms.DateInput(attrs={'class':'form-control','type':'date'},format='%Y-%m-%d'),
	    	'gender':forms.RadioSelect(choices=CHOICES),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'avatar':forms.FileInput(attrs={'class':'','id':'validatedInputGroupCustomFile'}),
	    }
    
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['class']=forms.ModelChoiceField(label='Класс',queryset=Classes.objects.filter(institution=user.institution))
        
        self.fields['class'].widget.attrs['class']='form-control'

