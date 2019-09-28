from django.urls import path
from .views import candidateHome, candidateCourse
from django.conf.urls import url

urlpatterns = [
    url(r'^$', candidateHome, name ="candidateHome"),
    url(r'^course/$', candidateCourse, name ="candidateCourse")
    #/(?P<id>\d+)/
]
