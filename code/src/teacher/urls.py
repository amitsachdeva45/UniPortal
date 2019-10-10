from django.urls import path
from .views import teacherCourse, teacherHome

from django.conf.urls import url

urlpatterns = [
    url(r'^$', teacherHome, name ="teacherHome"),
    url(r'^course/$', teacherCourse, name ="teacherCourse")
]