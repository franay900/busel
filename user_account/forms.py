from django import forms
from user_account.models import UserNet
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from institutions.models import TypeInstitutions
from django.contrib.auth.forms import SetPasswordForm
   
class UserEditForm(forms.ModelForm):
    
    class Meta:
        CHOICES =(
            ("мужской", "мужской"),
            ("женский", "женский"),
 
        )
  
        model = UserNet
        fields=['last_name','first_name','middle_name','gender','birth_day','groups','position','avatar','email']
        
   
        widgets={
	    	'last_name':forms.TextInput(attrs={'class':'form-control'}),
	    	'first_name':forms.TextInput(attrs={'class':'form-control'}),
	    	'middle_name':forms.TextInput(attrs={'class':'form-control'}),
            'birth_day':forms.DateInput(attrs={'class':'form-control','type':'date'},format='%Y-%m-%d'),
            'gender':forms.RadioSelect(choices=CHOICES),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'avatar':forms.FileInput(attrs={'class':'','id':'validatedInputGroupCustomFile'}),
            'position':forms.TextInput(attrs={'class':'form-control'}),
	    }
    
    
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(UserEditForm, self).__init__(*args, **kwargs)

        if self.current_user:
            self.typeInstitutions=self.current_user.pk
            Institutions=TypeInstitutions.objects.filter(pk=self.typeInstitutions).values('group')
            groupsUser=[]
            for i in Institutions:
                groupsUser.append(i['group'])
            self.fields["groups"] = forms.ModelMultipleChoiceField(
                    queryset=Group.objects.filter(pk__in=groupsUser),
                    label='Роли пользователя',
                    widget=forms.CheckboxSelectMultiple,
                    required=True)

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(),label='Пароль')
    

    class Meta:
        model = UserNet
        fields=['last_name','first_name','middle_name','avatar','email','username','password']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class SetPassword(SetPasswordForm):
    # Your declared form fields here
    ...

    def __init__(self, *args, **kwargs):
        super(SetPassword, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class EditMyAccountForm(forms.ModelForm):
    class Meta:
        model = UserNet
        fields=['last_name','first_name','middle_name','birth_day','gender','avatar', 'email']


        CHOICES =(
            ("мужской", "мужской"),
            ("женский", "женский"),
 
        )
  

        
   
        widgets={
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'middle_name':forms.TextInput(attrs={'class':'form-control'}),
            'birth_day':forms.DateInput(attrs={'class':'form-control','type':'date'},format='%Y-%m-%d'),
            'gender':forms.RadioSelect(choices=CHOICES),
            'avatar':forms.FileInput(attrs={'class':'','id':'validatedInputGroupCustomFile'}),
            # 'position':forms.TextInput(attrs={'class':'form-control'}),
        }
    


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        if 'instance' in kwargs:
            user = kwargs.pop('instance')
        else:
            user = False

        if not user.is_superuser:

            self.fields['last_name'].disabled=True
            self.fields['first_name'].disabled=True
            self.fields['middle_name'].disabled=True