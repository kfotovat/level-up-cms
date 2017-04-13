from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^mission-statement/$', views.MissionStatement.as_view(), name='mission-statement'),
    url(r'^enroll-your-school/$', views.EnrollYourSchool.as_view(), name='enroll'),
    url(r'^more-info/$', views.MoreInfo.as_view(), name='more-info'),
    url(r'^(?P<school_slug>[a-z-]+)/(?P<login_type>\w+)/(?P<username>\w+)/welcome/$', views.Welcome.as_view(), name='welcome'),
    url(r'^(?P<school_slug>[a-z-]+)/(?P<login_type>\w+)/(?P<username>\w+)/my-courses/$', views.TeacherCourseList.as_view(), name='teacher-courses'),
    url(r'^(?P<school_slug>[a-z-]+)/(?P<login_type>\w+)/(?P<username>\w+)/my-courses/(?P<pk>\d+)/$', views.TeacherCourseDetail.as_view(), name='course-detail'),
    url(r'^(?P<school_slug>[a-z-]+)/(?P<login_type>\w+)/(?P<username>\w+)/my-courses/add-course/$', views.AddCourse.as_view(), name='add-course'),
    url(r'^(?P<school_slug>[a-z-]+)/(?P<login_type>\w+)/(?P<username>\w+)/my-courses/(?P<pk>\d+)/update/$', views.UpdateCourseInfo.as_view(), name='update-course'),
    # url(r'^(?P<school_slug>[a-z-]+)/(?P<login_type>\w+)/(?P<username>\w+)/my-courses/(?P<pk>\d+)/delete/$', views.DeleteCourse.as_view(), name='delete-course'),
    url(r'^my-courses/(?P<pk>\d+)/$', views.TeacherCourseDetail.as_view(), name='course-detail'),
    url(r'^(?P<school_slug>[a-z-]+)/(?P<login_type>\w+)/(?P<username>\w+)/my-courses/(?P<pk>\d+)/my-students/$', views.CourseStudents.as_view(), name='course-students'),
    # url(r'^teachers/(?P<username>\w+)/welcome/$', views.Welcome.as_view(), name='student-current-progress'),
    url(r'^(?P<school_slug>[a-z-]+)/(?P<login_type>\w+)/(?P<username>\w+)/my-courses/(?P<pk>\d+)/my-students/(?P<student>\w+)/current-progress$', views.CurrentProgress.as_view(), name='student-current-progress'),
    url(r'^(?P<school_slug>[a-z-]+)/(?P<login_type>\w+)/(?P<username>\w+)/my-courses/(?P<pk>\d+)/my-students/(?P<student>\w+)/recent-progress$', views.RecentProgressHistory.as_view(), name='student-progress-history'),
    # url(r'^teachers/(?P<username>\w+)/welcome/$', views.Welcome.as_view(), name='add-student'),

    # url(r'^teachers/(?P<username>\w+)/welcome/$', views.Welcome.as_view(), name='welcome'),
    # url(r'^(?P<school_slug>\w+)/(?P<login_type>\w+)/(?P<username>\w+)/welcome/$', views.welcome, name='welcome'),
]
