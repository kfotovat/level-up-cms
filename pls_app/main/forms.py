from django import forms
from django.forms.widgets import Select, RadioSelect, Textarea
from .models import Student, Teacher, School, Course
# # from crispy_forms.helper import FormHelper
# # from crispy_forms.layout import Layout, Fieldset, MultiField, Submit, Button
# # from crispy_forms.bootstrap import *
#
# # form based on existing model
class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = "__all__"
	
# class StudentForm(forms.ModelForm):
# 	class Meta:
# 		model = Student
# 		fields = ['get_full_name', 'email', 'school_site']
# 	grade = forms.IntegerField()
# 		#can also specify exclude = []
#
# 	def clean_email(self):
# 		email = self.cleaned_data.get('email')
# 		email_handle, provider = email.split("@")
# 		domain, extension = provider.split(".")
# 		if extension != 'edu':
# 			raise forms.ValidationError("Please register using your .edu email address")
# 		return email
#
# # custom form
# class TeacherForm(forms.ModelForm):
# 	GRADE_CHOICES = (
# 		('PreSchool','PreSchool'),
# 		('Kindergarten','Kindergarten'),
# 		(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),
# 		(6,'6'),(7,'7'),(8,'8'),
# 		(9,'9'),(10,'10'),(11,'11'),(12,'12')
# 		)
#
# 	class Meta:
# 		model = Teacher
# 		fields = ['get_full_name', 'email', 'school_site']
# 	grade = forms.MultipleChoiceField(label="grade(s)",widget=forms.CheckboxSelectMultiple, choices=GRADE_CHOICES)
# 	number_courses = forms.IntegerField()
#
# class TeacherScheduleForm(forms.ModelForm):
# 	class Meta:
# 		model = Teacher
# 		fields = ['get_full_name', 'email', 'school_site']
#
#
# class SchoolForm(forms.ModelForm):
# 	class Meta:
# 		model = SchoolSite
# 		exclude = []
# 	referral = forms.CharField(widget=forms.Textarea)
# 	num_particip_teachers = forms.IntegerField()
# 	num_particip_students = forms.IntegerField()
#
# 	# phone validator
# 	contact_phone = forms.RegexField(regex=r'^\d{10}$'
#     # ,error_message = ("Please enter with area code, and no punctuation, in the following format: '8005551234'. Up to 10 digits allowed.")
#     )
#
#
# # class HorizRadioRenderer(RadioSelect.renderer):
# #     """ this overrides widget method to put radio buttons horizontally
# #         instead of vertically.
# #     """
# #     def render(self):
# #             """Outputs radios"""
# #             return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
#
# # class HorizRadioSelect(RadioSelect):
# #     renderer = HorizRadioRenderer
# # class ProgressVars():
# # 	CHOICES = ((True,'Yes'),(False,'No'))
# # 	LEVEL_CHOICES = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'))
# # 	behavior = forms.TypedChoiceField(label="Behavior Level",coerce=lambda x: int(x),widget=forms.RadioSelect(choices=LEVEL_CHOICES), required=True)
# # 	on_time = forms.TypedChoiceField(label="Arrives to Class On-Time",widget=forms.Select(choices=CHOICES),initial=True,required=True)
# # 	electronics = forms.TypedChoiceField(label="Proper Use of Electronics",widget=forms.Select(choices=CHOICES),initial=True,required=True)
# # 	personal_goals = forms.TypedChoiceField(label="Working Toward Personal Goals",widget=forms.Select(choices=CHOICES),initial=True,required=True)
# # 	leaving_class = forms.TypedChoiceField(label="Leaves Class Appropriately",widget=forms.Select(choices=CHOICES),initial=True,required=True)
# #
# #
# # class TeacherProgressForm(forms.ModelForm):
# # 	class Meta:
# # 		CHOICES = ((True,'Yes'),(False,'No'))
# # 		LEVEL_CHOICES = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'))
# #
# # 		model = Progress
# # 		fields = ['student_name', 'teacher_name', 'class_date', 'behavior', 'on_time', 'electronics', 'personal_goals', 'leaving_class', 'teacher_comments']
# #  		widgets = {
# #             # 'teacher_comments': Textarea(attrs={'cols': 80, 'rows': 20}),
# #             # 'behavior': Select(choices=LEVEL_CHOICES),
# #             'behavior': RadioSelect(choices=LEVEL_CHOICES),
# #             'leaving_class': RadioSelect(choices=CHOICES)
# #         }
# #         labels = {
# #             'personal_goals': 'Working Toward Personal Goals'
# #         }
# #         help_texts = {
# #             'behavior': 'see Behavior Level descriptions below'
# #         }
# #         error_messages = {}
# #
# #
# # class ProgressForm(forms.ModelForm):
# # 	class Meta:
# # 		CHOICES = ((True,'Yes'),(False,'No'))
# # 		LEVEL_CHOICES = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'))
# #
# # 		model = Progress
# # 		fields = ['student_name', 'teacher_name', 'class_date', 'behavior', 'on_time', 'electronics', 'personal_goals', 'leaving_class', 'teacher_comments']
# #  		widgets = {
# #             # 'teacher_comments': Textarea(attrs={'cols': 80, 'rows': 20}),
# #             # 'behavior': Select(choices=LEVEL_CHOICES),
# #             'behavior': RadioSelect(choices=LEVEL_CHOICES),
# #             'leaving_class': RadioSelect(choices=CHOICES)
# #         }
# #         labels = {
# #             'personal_goals': 'Working Toward Personal Goals'
# #         }
# #         help_texts = {
# #             'behavior': 'see Behavior Level descriptions below'
# #         }
# #         error_messages = {}
