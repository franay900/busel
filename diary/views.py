from django.shortcuts import render
from django.views.generic import View
from classes.models import Student,Load,StudentSubgroup
from datetime import datetime, timedelta,date
from modules.weeks import get_dates
from django.db.models import Q
from institutions.models import Periods


class Home(View):

	template_name = 'diary/home.html'

	def get(self,request):
		student = Student.objects.get(user=self.request.user)
		context = {}
		context['title'] = 'Дневник'
		context['student'] = student
		days = {0: u"Понедельник", 1: u"Вторник", 2: u"Среда", 3: u"Четверг", 4: u"Пятница", 5: u"Суббота", 6: u"Воскресенье"}
		context['days'] = days
		now = datetime.now().date()


		get_day =self.request.GET.get('day')
		if get_day:
			
			now = datetime.strptime(get_day, '%Y-%m-%d').date()
		monday = (now - timedelta(days = now.weekday()))
		sunday = (now + timedelta(days = 6 - now.weekday()))
		future_day = now + timedelta(days = 7)
		last_day = now - timedelta(days = 7)
		context['last'] = last_day
		context['future'] = future_day
		dates = get_dates(monday.strftime("%d.%m.%Y"),sunday.strftime("%d.%m.%Y"))
		
		arr = []
		num = 0
		for datea in dates:
			if num!=6:
				arr.append([datea,days[num]])
			num+=1
		context['dates'] = arr
		return render(request, self.template_name,context)


class GradeReport(View):
	template_name = 'diary/grade.html'

	def get(self,request):
		student = Student.objects.get(user=self.request.user)
		class_student = student.class_pk
		subgroups = StudentSubgroup.objects.filter(student=student)
		arr = []
		for subroup in subgroups:
			arr.append(subroup.subgroup.pk)
		get_subject = Load.objects.filter(Q(subgroup__pk=None) | Q(subgroup__pk__in=arr),class_pk=class_student)
		get_period = Periods.objects.filter(profile=class_student.period_profile)
		if request.GET.get('period'):
			now_period = Periods.objects.get(pk=int(request.GET.get('period')))
		else:
			now_period = get_period.first()
		context = {}
		if request.GET.get('year'):
			context['year'] = True 
		else:
			context['year'] = False
		context['title'] = 'Табель успеваемости'
		context['student'] = student
		context['subjects'] = get_subject
		context['period'] = now_period
		context['periods'] = get_period
		return render(request, self.template_name,context)


