from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

### Models needed ###
# Students - can have many courses
# Teachers - can have many courses (by ext many students)
# Course - fk to Teacher, course can have many students
# Schools = can have many teachers
# Admin staff??
# Progress
# BehaviorLevels


# Schools 	--> Admin
	      # --> Students(?)
	      # --> Teachers --> Courses (FK) --> Students --> Progress
		  			   # --> BehaviorLevels

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email = models.EmailField(null=False)
	first_name = models.CharField(max_length=30, null=False)
	last_name = models.CharField(max_length=30, null=False)
	full_name = models.CharField(max_length=70, null=True, blank=True)
	school_site = models.ForeignKey("SchoolSite", null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def save(self, *args, **kwargs):
		full_name = "{} {}".format(self.first_name, self.last_name)
		self.full_name = full_name
		super(Profile, self).save(*args, **kwargs)

	class Meta:
		abstract = True

# signals hooking new user creation / update to new profile creation / update
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Student(Profile):

	def group(self):
		return "students"

	def __unicode__(self): #Python 3.X is __str__
		return self.full_name

	courses = models.ManyToManyField("Course")


class Teacher(Profile):

	def group(self):
		return "teachers"

	def __unicode__(self): #Python 3.X is __str__
		return self.full_name

class SchoolSite(models.Model):
	school_site = models.CharField(max_length=100, default="Demo School")
	school_slug = models.SlugField(max_length=100, blank=True)
	school_type = models.CharField(max_length=50)
	address1 = models.CharField(max_length=50)
	address2 = models.CharField(max_length=50, blank=True)
	city = models.CharField(max_length=50)
	contact_name = models.CharField(max_length=50, null=True)
	contact_phone = models.CharField(max_length=20, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def save(self, *args, **kwargs):
		if not self.pk:
			school_slug = slugify(self.school_site)
		super(SchoolSite, self, *args, **kwargs)

	def __unicode__(self): #Python 3.X is __str__
		return self.school_site


class Course(models.Model):
	course_name = models.CharField(max_length=50)
	# fk
	teacher_name = models.ForeignKey("Teacher", null=True, blank=True)
	# a course can have many times offered?
	block_order = models.PositiveIntegerField(default=1)
	start_time = models.TimeField(null=True)
	end_time = models.TimeField(null=True)

	# this sets the redirect after creating a new course
	def get_absolute_url(self):
		return reverse('course-detail', kwargs={'course_id':self.pk})

	def __unicode__(self): #Python 3.X is __str__
		return self.course_name


#
# class CourseStudents(models.Model):
# 	course_id = Course.pk
# 	student_id = Student.pk
#
# 	# sets redirect after adding a new course
# 	def get_absolute_url(self):
# 		return reverse('course-students', kwargs={'pk':self.pk})
#
#
#
# class Progress(models.Model):
# 	class_date = models.DateTimeField()
# 	status = models.CharField(max_length=30, default="Pending")
# 	submitted = models.DateTimeField(auto_now_add=True, auto_now=False)
# 	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
#
# 	behavior = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
# 	# BEHAVIOR_CHOICES = (1, 2, 3, 4, 5)
# 	# behavior2 = models.PositiveIntegerField(choices=BEHAVIOR_CHOICES)
# 	on_time = models.BooleanField(default=True)
# 	electronics = models.BooleanField(default=True)
# 	personal_goals = models.BooleanField(default=True)
# 	leaving_class = models.BooleanField(default=True)
# 	teacher_comments = models.TextField()
#
# 	# fk
# 	student_name = models.ForeignKey("Student", null=True, blank=True)
# 	teacher_name = models.ForeignKey("Teacher", null=True, blank=True)
#
# 	def __unicode__(self):
# 		return self.student_name + " - " + self.class_date
#
#
# # break each level out into a level class(number, description)?
# class BehaviorLevelsDefinition(models.Model):
# 	custom_name = models.CharField(max_length=40, null=False)
# 	level1 = models.TextField()
# 	level2 = models.TextField()
# 	level3 = models.TextField()
# 	level4 = models.TextField()
# 	level5 = models.TextField()
# 	default_weights = {5:100, 4:80, 3:60, 2:40, 1:20}
# 	weights = {}
#
# 	def __unicode__(self):
# 		return self.custom_name
