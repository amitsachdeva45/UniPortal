from django.urls import path
from .views import candidateHome, candidateCourse, candidateFetchCourse
from django.conf.urls import url

urlpatterns = [
    url(r'^$', candidateHome, name ="candidateHome"),
    url(r'^course/$', candidateCourse, name ="candidateCourse"),
    url(r'^fetchCourse/$', candidateFetchCourse, name ="candidateFetchCourse")
    #/(?P<id>\d+)/
]
