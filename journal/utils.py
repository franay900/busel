from .models import Load
from classes.models import Classes, Student
from institutions.models import Periods
from journal.models import Lessons, Marks
from django.db.models import Q, Sum


class Journal():

	def get_student(self):
		return Student.objects.filter(class_pk=self.get_class(),user__isnull=False).order_by('user')

	def check_admin(self):
		return self.request.user.groups.filter(pk__in=[1]).first()

	def get_classes(self):
	    return Classes.objects.filter(institution=self.request.user.institution)

	def get_class(self):
	    if 'load' in self.request.POST:
	        load = self.request.POST.get("load")
	        get_load = Load.objects.get(pk=load)
	        return Classes.objects.get(pk=get_load.class_pk.pk)
	    else:
	        return Classes.objects.filter(institution=self.request.user.institution).first()

	def get_load(self):


	    if 'load' in self.request.POST:
	        load = self.request.POST.get("load")
	        return Load.objects.get(pk=load)
	    else:
	        if self.check_admin():
	            return Load.objects.filter(class_pk__in=self.get_classes()).first()

	        else:
	            return Load.objects.filter(class_pk=self.get_class(), teacher=self.request.user).order_by('class_pk',
	                                                                                                      'subject_pk').first()

	def get_loads(self):

	    if self.check_admin():
	        return Load.objects.filter(class_pk=self.get_classes().first()).order_by('class_pk', 'subject_pk',
	                                                                                 'subgroup')
	    else:
	        lessons=Lessons.objects.filter(teacher=self.request.user,class_pk__in=self.get_classes()).distinct('subject_pk').values_list('subject_pk')
	        return Load.objects.filter(Q(pk__in=lessons) or Q(teacher=self.request.user)).order_by('class_pk', 'subject_pk', 'subgroup')

	def get_period(self):
	    if 'period' in self.request.POST:
	        period = self.request.POST.get("period")
	        periods = Periods.objects.get(pk=period)
	        return periods
	    else:
	        return Periods.objects.filter(profile=self.get_class().period_profile)

	def get_lessons(self):
		date_start=self.get_period().start
		date_end=self.get_period().end
		if self.check_admin():

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
