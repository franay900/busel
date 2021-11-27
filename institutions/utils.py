from institutions.models import PeriodProfile,Periods



class Study_Periods():
	def get_period_profile(self):
		return PeriodProfile.objects.get(pk=self.kwargs['profile_pk'])

	def get_periods(self):
		return Periods.objects.filter(profile=self.get_period_profile()).order_by("start")
	def get_update_period(self):
		for period in self.get_periods():
			start_period=self.request.POST.get('start'+str(period.pk))
			end_period=self.request.POST.get('end'+str(period.pk))
			period.start=start_period
			period.end=end_period
			period.save()