from django.urls import path
from .views import candidateHome, candidateCourse, candidateFetchCourse, candidateFetchEachSemCourse, selectCourse, fetchNotification, payfees

from django.conf.urls import url

urlpatterns = [
    url(r'^$', candidateHome, name ="candidateHome"),
    url(r'^course/$', candidateCourse, name ="candidateCourse"),
    url(r'^fetchCourse/$', candidateFetchCourse, name ="candidateFetchCourse"),
    url(r'^fetchCourseSemester/(?P<id>\d+)/$', candidateFetchEachSemCourse, name ="candidateFetchEachSemCourse"),
    url(r'^selectCourse/$', selectCourse, name ="selectCourse"),
    url(r'^notification/$', fetchNotification, name ="fetchNotification"),
    url(r'^fees/$', payfees, name ="payfees")
    #/(?P<id>\d+)/
]
