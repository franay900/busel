from django.shortcuts import render
from django.views.generic import View
from user_account.models import UserNet
from classes.models import Load
from journal.models import Lessons,Marks


class ReportsView(View):
	def get(self,request):
		context={}
		context['title']="Отчеты"
		return render(request,'reports/reports.html',context)



class ReportJournal(View):
	def get(self,request):
		lists=[]
		loads_array=[]
		a=0
		count_mark=0
		mark_count=0
		teachers=UserNet.objects.filter(institution=request.user.institution,groups=2,is_active=True)
		for teacher in teachers:
			
			loads=Load.objects.filter(teacher=teacher).order_by("class_pk","subject_pk","subgroup")
			if loads:
				for load_list in loads:
					lessons=Lessons.objects.filter(subject_pk=load_list).order_by("date")
					count_lessons=lessons.count()
					count_lessons_with_topic=Lessons.objects.filter(subject_pk=load_list,topic__isnull=False).exclude(topic='').count()
					count_lessons_with_homework=Lessons.objects.filter(subject_pk=load_list,homework__isnull=False).exclude(homework='').count()
					count_mark=0
					for lesson in lessons:
						mark_count=Marks.objects.filter(lesson=lesson).first()

						if mark_count!=None:
							count_mark+=1
					if int(count_mark)!=0 and int(count_lessons)!=0:
						percent_marks=round(int(count_mark)/int(count_lessons)*100)
					else:
						percent_marks=0
					if int(count_lessons_with_topic)!=0 and int(count_lessons)!=0:
						percent_topics=round(int(count_lessons_with_topic)/int(count_lessons)*100)
					else:
						percent_topics=0
					if int(count_lessons_with_homework)!=0 and int(count_lessons)!=0:
						percent_homework=round(int(count_lessons_with_homework)/int(count_lessons)*100)
					else:
						percent_homework=0

					loads_array.append([[load_list],[percent_topics],[percent_marks],[percent_homework]])
					# print(count_lessons,teacher,load_list.subject_pk)
				lists.append([[teacher],[loads_array]])
				loads_array=[]
				
				count_mark,mark_count=0,0
				a+=1
				
		
		context={}
		context['title']="Отчет по ведению электронного журнала"
		context['result']=lists
		return render(request,'reports/report_journal.html',context)