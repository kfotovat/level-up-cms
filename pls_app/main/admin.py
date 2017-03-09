# import django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile, Course, School

# django.setup()
# from django.db.models.loading import cache as model_cache
# if not model_cache.loaded:
#     model_cache.get_models()

# User = settings.AUTH_USER_MODEL

class SchoolAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'city', 'contact_name']
	prepopulated_fields = {'slug': ('name',)}
	# form = SchoolForm

class UserAdmin(admin.ModelAdmin):
	list_display = ['get_full_name', 'username', 'email']

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'Profile'
	fk_name = 'user'

class CustomUserAdmin(UserAdmin):
	inlines = [ProfileInline,]

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# class TeacherAdmin(admin.ModelAdmin):
# 	list_display = ['__unicode__', 'email']
	# form = TeacherForm

# class StudentInline(admin.TabularInline):
#     model = Student
#     fk_name = 'courses'

class CourseAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'teacher_name', 'start_time', 'course_name']
	# inlines = [StudentInline]


# Register your models here.
admin.site.register(School, SchoolAdmin)
admin.site.unregister(User)
# admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, CustomUserAdmin)
# admin.site.register(Student)
# admin.site.register(Teacher)
admin.site.register(Course, CourseAdmin)
