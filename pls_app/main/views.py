from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Profile, School, Progress
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
# from .forms import StudentForm, TeacherForm

# , TeacherProgressForm, ProgressForm
# from .formsets import ProgressFormset, CourseFormset
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# shared helper methods
def get_credentials(view, dict={}):
    creds = view.request.user.profile.add_credentials_to_context(dict)
    return creds

def get_progress_data(student_username, course_id):
    student_user = User.objects.get(username=student_username)
    progress_history = Progress.objects.filter(course_name=course_id, student_name=student_user.profile)
    if not progress_history:
        return [{"status": "No data"}]
    return progress_history


# basic views
class Home(TemplateView):
    template_name = 'index.html'

class Welcome(LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'

    def credentials(self):
        return get_credentials(self)

# standard static content pages
class MissionStatement(TemplateView):
    template_name = 'standard_content.html'
    header = "Our Mission Statement"
    main_text = "Our goal is to provide students with a predictable routine \
    on a daily basis. Positive Level System enables students to monitor their \
    behavior and to learn strategies to better engage both socially and \
    academically on an hourly, daily, and weekly basis. Teachers can guide \
    students in school expectations and track behavior data throughout the \
    school day. Used with fidelity, PLS allows a common language for students \
    and teachers to use across the day in a variety of settings. Students are \
    positively reinforced for maintaining a set of school and classroom \
    expectations which enables them to feel safe and learn in a calm nurturing \
    environment."

class EnrollYourSchool(TemplateView):
    template_name = 'standard_content.html'
    header = "Enroll Your School"
    main_text = "PLS is currently implemented at elementary, middle, and \
    high schools in the Albuquerque region. If you are an interested school \
    teacher, classroom assistant, or part of the administrative staff, please \
    contact us for a consultation and we can help determine if PLS is a good \
    fit for your site."

class MoreInfo(TemplateView):
    template_name = 'standard_content.html'
    header = "More Information"
    main_text = "PLS is committed to fostering accountability in students and \
    empowering teachers and school staff to responsibly set and regularly \
    achieve fluid goals appropriate to your classroom. Our service is a multi-\
    level, fully customizable, data-driven solution comprising quantitative \
    assessment, qualitative and narrative feedback, short-term and long-term \
    student incentives, and longitudinal reporting and analytics. Check out \
    our demo video and see the wide array of resources PLS can bring to your \
    classroom."

# #create login function that redirects user to her specific detail page
# # class Login(generic.TemplateView):
# #     template_name = 'login.html'
# #
# # class Logout(generic.TemplateView):
# #     template_name = 'logout.html'
#
# working querysets:
# all_courses = Course.objects.all()
# origami = Course.objects.get(course_name='Origami')
# origami_list = Course.objects.filter(course_name='Origami')
# origami_students = Profile.objects.filter(courses__in=origami)
# origami_students = origami.profile_set.all()

# riemen = User.objects.filter(first_name='Jennifer',last_name='Riemen')
# riemen = User.objects.get(username='jriemen')
# riemen_courses = Course.objects.filter(teacher_name=riemen.profile)
# riemen_students = Profile.objects.filter(role=1,courses__in=riemen_courses)
#
# kdurant = User.objects.get(username='kdurant')
# kdurant_courses = kdurant.profile.courses.all()
# kdurant_teachers = [course.teacher_name for course in kdurant_courses]
#
#
# generic and class-based views
class TeacherCourseList(ListView):
    model = Course
    template_name = "teachers/teacher_courses.html"

    def teacher_courses(self):
        teacher = Profile.objects.get(user=self.request.user)
        return Course.objects.filter(teacher_name=teacher)


class TeacherCourseDetail(DetailView):
    model = Course
    template_name = "teachers/course_detail.html"


class AddCourse(CreateView):
    model = Course
    fields = "__all__"
    template_name = "teachers/course_form.html"

    def form_valid(self, form):
        form.instance.teacher_name = self.request.user.profile
        return super(AddCourse, self).form_valid(form)


class UpdateCourseInfo(UpdateView):
    model = Course
    fields = "__all__"
    template_name = "teachers/course_form.html"


class CourseStudents(ListView):
    model = Profile
    template_name = "teachers/course_students.html"
    # course_students_current_progress = None
    # course_students_all_progress = None

    def current_course(self):
        return Course.objects.get(pk=self.kwargs['pk'])

    def current_course_pk(self):
        current_course = Course.objects.get(pk=self.kwargs['pk'])
        return current_course.pk

    def course_students_all_progress(self):
        current_course = Course.objects.get(pk=self.kwargs['pk'])
        course_students = current_course.profile_set.all()
        if not course_students:
            return []
        # course_students_all_progress = [(student, get_progress_data(student.user.username, self.kwargs['pk'])) for student in course_students]
        # self.course_students_all_progress = course_students_all_progress
        # self.course_students_current_progress = [(student, progress[0]) for student, progress in course_students_all_progress]
        return [(student, get_progress_data(student.user.username, self.kwargs['pk'])) for student in course_students]

    def course_students_current_progress(self):
        current_course = Course.objects.get(pk=self.kwargs['pk'])
        course_students = current_course.profile_set.all()
        if not course_students:
            return []
        course_students_all_progress = [(student, get_progress_data(student.user.username, self.kwargs['pk'])) for student in course_students]
        return [(student, progress[0]) for student, progress in course_students_all_progress if progress]

    # def course_students_progress(self):
        # self.course_students_progress = [get_progress_data(student.user.username, self.current_course_pk) for student in self.course_students]
        # return [get_progress_data(student.user.username, self.current_course_pk) for student in self.course_students]
        # return Progress.objects.filter(course=self.current_course)
    #
    # def get_queryset(self):
    #     # course = self.current_course
    #     current_course = Course.objects.get(pk=self.kwargs['pk'])
    #     self.course_students = current_course.profile_set.all()
    #     return current_course.profile_set.all()

class RecentProgressHistory(ListView):
    model = Progress
    fields = "__all__"
    template_name = "teachers/student_progress_history.html"
    context_object_name = "recent_progress_history"
    all_progress_history = None
    recent_progress_history = None
    current_progress = None
    all_progress_history_length = 0

    def get_queryset(self, *args, **kwargs):
        # limit query to 10(?) most recent progresses by given student
        student_username = self.kwargs['student']
        course_id = self.kwargs['pk']
        progress_history = get_progress_data(student_username, course_id)
        # student_user = User.objects.get(username=student_username)
        # progress_history = Progress.objects.filter(course_name=self.kwargs['pk'], student_name=student_user.profile)
        self.all_progress_history = progress_history[6:]
        self.recent_progress_history = progress_history[1:6]
        self.current_progress = progress_history[0]
        self.all_progress_history_length = len(progress_history)
        return progress_history

    def get_context_data(self, *args, **kwargs):
        context = super(RecentProgressHistory, self).get_context_data(*args, **kwargs)
        context = self.request.user.profile.add_credentials_to_context(context)
        context['student'] = self.kwargs['student']
        return context

# need to fix this guy
# class DeleteCourse(DeleteView):
#     model = Course
#     # fields = "__all__"
#     success_url = reverse_lazy('teacher-courses', kwargs=context)
#
#     def credentials(self):
#         return get_credentials(self)

    # def get_object(self, queryset=None):
    #     obj = super(DeleteCourse, self).get_object()
    #     if not obj.owner == self.request.user:
    #         raise Http404
    #     return obj

    # def get_queryset(self):
    #     qs = super(DeleteCourse, self).get_queryset()
    #     qs = qs.filter(owner=self.request.user)
    #     if not qs:
    #         raise Http404
    #     return qs

    #     user = self.request.user.profile
    #     context = user.add_credentials_to_context({'pk':self.kwargs['pk']})
    #     print "queryset:", queryset
    #     print "context:", context
    #     return context
    #
    # def delete(self, request, *args, **kwargs):
    #     course_to_delete = Course.objects.get(pk = self.kwargs['pk'])
    #     course_to_delete.delete()
    #
    #     user = request.user.profile
    #     context = user.add_credentials_to_context({'pk':self.kwargs['pk']})
    #     return HttpResponseRedirect(reverse_lazy('teacher_courses', kwargs=context))

# class AddStudent(generic.edit.CreateView):
#     model = Student
#     fields = "__all__"
#     template_name = "teachers/student_form.html"
#
class CourseDetail(DetailView):
    pass

# def auth_view(request):
#     email = request.POST.get('email', None)
#     password = request.POST.get('password', None)
#     user = auth.authenticate(email=email, password=password)
#
#     if user:
#         auth.login(request, user)
#         return HttpResponseRedirect('logged_in')
#     else:
#         return HttpResponseRedirect('invalid_login')
#
# # def progressStudent(request):
# #     # form = ProgressForm(request.POST or None)
# #     form = ProgressForm(request.POST or None)
# #     context = {
# #         "form": form
# #     }
# #     return render(request, "progress-student-full.html", context)
# #
# # def progressTeacher(request):
# #     # form = ProgressForm(request.POST or None)
# #     form = ProgressForm(request.POST or None)
# #     context = {
# #         "form": form
# #     }
# #     return render(request, "progress-teacher-full.html", context)
# #
# # def progressform(request):
# #     # form = ProgressForm(request.POST or None)
# #     form = ProgressForm(request.POST or None)
# #     context = {
# #         "form": form,
# #     }
# #     return render(request, "progressform.html", context)
#
#
# # def progressFormset(request):
# #     student_queryset = Student.objects.all()
# #     teacher_queryset = Teacher.objects.all()
# #     form = TeacherForm(request.POST or None)
# #     course_formset = CourseFormset(request.POST or None)
# #     progress_formset = ProgressFormset(request.POST or None)
# #     context = {
# #         "teacher_form": form,
# #         "course_formset": course_formset,
# #         "progress_formset": progress_formset,
# #     }
# #     return render(request, "formset.html", context)
#
# def add_courses(request):
#     # initial queryset (empty)
#     initial_queryset = Teacher.objects.none()
#     # set queryset to just Sunita
#     teacher_queryset = Teacher.objects.filter(full_name__startswith='Sunita')
#
#     teacher_form = TeacherForm(request.POST or None)
#     course_formset = CourseFormset(request.POST or None)
#
#     if request.method == "POST":
#         # else replace first 2 params with request.POST and request.FILES
#         course_formset = course_formset(None, None, queryset=teacher_queryset)
#         if course_formset.is_valid():
#             course_formset.save()
#             # Do something.
#         else:
#             course_formset = course_formset(queryset=initial_queryset)
#
#     context = {
#         "course_formset": course_formset,
#         "teacher_form": teacher_form,
#     }
#
#     return render(request, "add-courses.html", context)
