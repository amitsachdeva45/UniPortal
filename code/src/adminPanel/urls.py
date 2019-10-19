from django.urls import path
from .views import adminHome, adminCourse, deleteCourse
from django.conf.urls import url

urlpatterns = [
    url(r'^$', adminHome, name ="adminHome"),
    url(r'^course/$', adminCourse, name ="adminCourse"),
    url(r'^deleteCourse/(?P<id>\d+)/$', deleteCourse, name="deleteCourse"),
    #/(?P<id>\d+)/
]
