from __future__ import unicode_literals

from django.db import models
# from django.conf import settings
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


# Schools 	--> School Staff
	      # --> Students
	      # --> Teachers --> Courses (FK) --> Students --> Progress
		  			   # --> BehaviorLevels

class Profile(models.Model):
	ROLES_CHOICES = (
		(1, 'Student'),
		(2, 'Teacher')
	)
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		primary_key=True)
	school = models.ForeignKey("School", null=True, blank=True)
	role = models.PositiveSmallIntegerField(choices=ROLES_CHOICES, null=True, blank=True)
	courses = models.ManyToManyField("Course", null=True, blank=True)

	def __unicode__(self):
		return self.user.get_full_name()

	def get_role(self):
		if self.role == 1:
			return "students"
		if self.role == 2:
			return "teachers"

	def is_student(self):
		return self.role == 1

	def is_teacher(self):
		return self.role == 2

	def add_credentials_to_context(self, context_dict):
	    temp = {}
	    temp['username'] = self.user.username
	    temp['school_slug'] = self.user.profile.school.slug
	    temp['login_type'] = self.user.profile.get_role()
	    new_dict = dict(context_dict, **temp)
	    return new_dict

	# class Meta:
	# 	abstract = True

# signals hooking new user creation / update to new profile creation / update
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
# 	if created:
# 		Profile.objects.create(user=instance)
# 	instance.profile.save()

# class Student(Profile):
#
# 	courses = models.ManyToManyField("Course", null=True, blank=True)
#
# 	def __unicode__(self):
# 		return self.user.get_full_name()
#
#
# class Teacher(Profile):
#
# 	courses = models.ManyToManyField("Course", null=True, blank=True)
#
# 	def __unicode__(self):
# 		return self.user.get_full_name()


# signals hooking new user creation / update to new profile creation / update
# @receiver(post_save, sender=User)
# def create_or_update_user_teacher(sender, instance, created, **kwargs):
# 	if created:
# 		Teacher.objects.create(user=instance)
# 	instance.teacher.save()

class School(models.Model):
	PRIMARY = 1
	MIDDLE = 2
	HIGH = 3
	SCHOOL_TYPE_CHOICES = (
		(PRIMARY, 'Primary School'),(MIDDLE, 'Middle School'),(HIGH, 'High School'),
		)

	name = models.CharField(max_length=100, default="Demo School")
	slug = models.SlugField(max_length=100, blank=True, unique=True)
	school_type = models.PositiveSmallIntegerField(choices=SCHOOL_TYPE_CHOICES, blank=True)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	contact_name = models.CharField(max_length=50, null=True)
	contact_phone = models.CharField(max_length=20, null=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.pk:
			self.slug = slugify(self.name)
		super(School, self, *args, **kwargs)

	def __unicode__(self): #Python 3.X is __str__
		return self.name


class Course(models.Model):
	course_name = models.CharField(max_length=50)
	# fk
	teacher_name = models.ForeignKey("Profile", null=True, blank=True, on_delete=models.CASCADE, limit_choices_to={'role': 2})
	# a course can have many times offered?
	block_order = models.PositiveIntegerField(default=1)
	start_time = models.TimeField(null=True)
	end_time = models.TimeField(null=True)

	# this sets the redirect after creating/updating a new course
	def get_absolute_url(self):
		return reverse('course-detail', kwargs={'pk': self.pk})

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



class Progress(models.Model):
	PENDING = 1
	SUBMITTED = 2
	EDITED = 3
	STATUS_CHOICES = (
		(PENDING, 'Pending'),(SUBMITTED, 'Submitted'),(EDITED, 'Edited'),
		)
	# class_date aka generated --progress won't be generated until class begins?
	class_date = models.DateTimeField()
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
	submitted = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	behavior = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	# BEHAVIOR_CHOICES = (
		# (1, ___),(2, ___),(3, ___),(4, ___),(5, ___)
		# )
	# behavior2 = models.PositiveIntegerField(choices=BEHAVIOR_CHOICES)
	on_time = models.BooleanField(default=True)
	electronics = models.BooleanField(default=True)
	personal_goals = models.BooleanField(default=True)
	leaving_class = models.BooleanField(default=True)
	teacher_comments = models.TextField()

	# fk
	# must validate that this profile is a student
	student_name = models.ForeignKey("Profile", null=True, blank=True)
	course_name = models.ForeignKey("Course", null=True, blank=True)

	def __unicode__(self):
		return self.student_name + " - " + self.class_date


# break each level out into a level class(number, description)?
class BehaviorLevelsDefinition(models.Model):
	# must validate that this profile is a teacher
	created_by = models.ForeignKey("Profile", null=True, blank=True)
	custom_name = models.CharField(max_length=40, null=False)
	level1 = models.TextField()
	level2 = models.TextField()
	level3 = models.TextField()
	level4 = models.TextField()
	level5 = models.TextField()
	default_weights = {5:100, 4:80, 3:60, 2:40, 1:20}
	weights = {}

	def __unicode__(self):
		return self.custom_name
