from django.urls import path
from .views import *


urlpatterns=[
	path('',InstitutionsHomeView.as_view() ,name="institutionsHome"),
	path('study_periods',StudyPeriodsView.as_view() ,name="StudyPeriods"),
	path('add_periods',Add_periods.as_view() ,name="AddPeriods"),
	path('delete_profile_periods/<int:pk>/',DeleteProfilePeriods.as_view() ,name="Delete_profile_periods"),
	path('edit_periods',Add_periods.as_view() ,name="AddPeriods"),
	path('study_periods_update/<int:profile_pk>/',StudyPeriodsUpdateView.as_view() ,name="StudyPeriodsUpdate"),
	path('bell_profile_list/',BellProfileView.as_view() ,name="Bell_profile_list"),
	path('bell_profile_create/',BellProfileCreateView.as_view() ,name="Bell_profile_create"),
	path('subject/',SubjectView.as_view(),name="Subject_list"),
	path('delete_subject/<int:pk>/',DeleteSubject.as_view() ,name="Delete_subject"),

	path('profession/',ProfessionsView.as_view(),name="ProfessionList"),
	path('delete_profession/<int:pk>/',DeleteProfession.as_view() ,name="DeleteProfession"),
	#админка
	path('create_institution/',InstitutionCreate.as_view() ,name="InstitutionCreate"),
	path('block_institution/<int:institution>',BlockInstitution.as_view() ,name="BlockInstitution"),
	path('unblock_institution/<int:institution>',UnblockInstitution.as_view() ,name="UnBlockInstitution"),
	path('edit_institution/<int:pk>', EditInstitutuonView.as_view(), name="EditInstitution"),
	#

	path('ads/', AdsCreateView.as_view(), name='create_ad'),
	path('ads/delete/<int:pk>', AdsDeleteView.as_view(), name='delete_ads'), 

	path('translate_year/', TranslationOfTheYear.as_view(), name='translate_year')
]

