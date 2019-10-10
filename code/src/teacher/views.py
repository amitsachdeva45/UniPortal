from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.cache import cache
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse

def commonData():
    userData = cache.get("TeacherData")
    if userData == None:
        return False
    start_month = int(userData['date_of_joining'].strftime("%m"))
    start_year = int(userData['date_of_joining'].strftime("%Y"))
    cur_month = int(datetime.now().date().strftime("%m"))
    cur_year = int(datetime.now().date().strftime("%Y"))
    userData['experience'] = ((cur_year-start_year)*12 + cur_month-start_month)/12.0
    context = {
        "userDetail": userData,
        "userId": cache.get("CandidateUserId"),
        "userName": userData['first_name'] + " " + userData['last_name']
    }
    return context
# Create your views here.
@login_required(login_url='/')
def teacherCourse(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    return render(request, "teacherCourse.html", {})

@login_required(login_url='/')
def teacherHome(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    return render(request, "teacherHome.html", context)