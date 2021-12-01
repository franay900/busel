from .models import Load
from classes.models import Classes, Student, StudentSubgroup
from institutions.models import Periods
from journal.models import Lessons, Marks
from django.db.models import Q, Sum


class Journal():
	type_journal='my'
	def check_admin(self):
		return self.request.user.groups.filter(pk__in=[1]).first()
	def get_context(self):
		context={}
		context['title'] = 'Журнал'
		if self.get_loads():
			context['lessons']=self.get_lessons()
			context['period']=self.get_period()
			context['periods']=Periods.objects.filter(profile=self.get_period().profile)
			context['loads']=self.get_loads()
			context['load_pk']=self.get_load()
			context['students']=self.get_student()
			context['classes']=self.get_classes()
			date_start=self.get_period().start
			date_end=self.get_period().end
			context['scores']=self.count_average_score()
			context['type_journal']=self.type_journal
		return context



	def get_classes(self):
	    return Classes.objects.filter(institution=self.request.user.institution).order_by('class_number','letter')

	def get_class(self):

		if 'load' in self.request.POST or 'load' in self.kwargs:
	    	
			if 'load' in self.request.POST:

				load = self.request.POST.get("load")
			if 'load' in self.kwargs:
				load = self.kwargs["load"]
			get_load = Load.objects.get(pk=load)
			return Classes.objects.get(pk=get_load.class_pk.pk)

		else:
			if  self.type_journal=='school':
				return Classes.objects.filter(institution=self.request.user.institution).first()
			else:
				return Classes.objects.get(pk=self.get_loads().first().class_pk.pk)


	def get_student(self):
		
		if not self.get_load().subgroup:
			return Student.objects.filter(class_pk=self.get_class(),user__isnull=False,user__is_active=True).order_by('user')
		else:

			subgroup_list=StudentSubgroup.objects.filter(subject=self.get_load().subject_pk, subgroup=self.get_load().subgroup).values_list('student')
			return Student.objects.filter(pk__in=subgroup_list)

	def get_loads(self):

	    if self.type_journal=='school':
	        return Load.objects.filter(class_pk=self.get_class()).order_by('class_pk', 'subject_pk',
	                                                                                 'subgroup')
	    else:
	        lessons=Lessons.objects.filter(teacher=self.request.user,class_pk__in=self.get_classes()).distinct('subject_pk').values_list('subject_pk')
	        return Load.objects.filter(Q(pk__in=lessons) | Q(teacher=self.request.user)).order_by('class_pk', 'subject_pk', 'subgroup')

	def get_load(self):


	    if 'load' in self.request.POST:
	        load = self.request.POST.get("load")
	        return Load.objects.get(pk=load)
	    else:
	        if self.type_journal=='school':
	            return Load.objects.filter(class_pk=self.get_class()).first()

	        else:
	            return self.get_loads().first()
	def get_period(self):

	    if 'period' in self.request.POST:
	        period = self.request.POST.get("period")
	        periods = Periods.objects.get(pk=period)
	        return periods
	    else:
	        return Periods.objects.filter(profile=self.get_class().period_profile).first()
	    
	def get_lessons(self):
		date_start=self.get_period().start
		date_end=self.get_period().end
		if  self.type_journal=='school':

			return Lessons.objects.filter(subject_pk=self.get_load(),date__range=[date_start,date_end]).order_by("date")
		else:

			if self.get_load().teacher==self.request.user:
				return Lessons.objects.filter(subject_pk=self.get_load(),date__range=[date_start,date_end]).order_by("date")
			else:
				return Lessons.objects.filter(subject_pk=self.get_load(),date__range=[date_start,date_end],teacher=self.request.user).order_by("date")

	def count_average_score(self):

		scores=[]
		# get_all_lessons=Lessons.objects.filter(subject_pk=self.get_load(),date__range=[date_start,date_end]).order_by("date")
		for student in self.get_student():
			scores.append(student.pk)
		return scores

class TimetableSettigns():
    def get_class(self):
        return Classes.objects.get(pk=self.request.POST.get("class"))
