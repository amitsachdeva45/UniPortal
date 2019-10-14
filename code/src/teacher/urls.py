from django.urls import path
from .views import teacherCourse, teacherHome, selectCandidate, submitScores, teacherNotification

from django.conf.urls import url

urlpatterns = [
    url(r'^$', teacherHome, name ="teacherHome"),
    url(r'^course/$', teacherCourse, name ="teacherCourse"),
    url(r'^notification/$', teacherNotification, name ="teacherNotification"),
    url(r'^selectCandidate/$', selectCandidate, name ="selectCandidate"),
    url(r'^submitScores/$', submitScores, name ="submitScores"),

]