from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.cache import cache
from datetime import datetime
from university.common_function import get_id, insert_one, get_all, get_find_one, update_one
from django.http import HttpResponseRedirect, HttpResponse
import json

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
        "userId": cache.get("TeacherUserId"),
        "userName": userData['first_name'] + " " + userData['last_name']
    }
    return context
# Create your views here.
@login_required(login_url='/')
def teacherCourse(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    data = dict()
    data['user_id'] = str(cache.get("TeacherUserId"))
    all_courses = get_all("course_teacher", data)
    final = list()
    for course in all_courses:
        temp = dict()
        temp['id'] = int(course['course_id'])
        one_course = get_find_one('courses', temp)
        temp['course_name'] = one_course['course_name']
        temp['branch_choice'] = one_course['branch_choice']
        temp['course_choice'] = one_course['course_choice']
        final.append(temp)
    context['courses'] = final
    return render(request, "teacherCourse.html", context)

@login_required(login_url='/')
def teacherHome(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    return render(request, "teacherHome.html", context)

def selectCandidate(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        data = dict()
        data['course_id'] = str(request.POST.get('course_id'))
        data['status'] = "incomplete"
        all_users = get_all("course_user", data)
        final = list()
        for user in all_users:
            temp = dict()
            temp['id'] = int(user['user_id'])
            score = user['scores']
            temp_user = get_find_one("auth_user", temp)
            temp['first_name'] = temp_user['first_name']
            temp['last_name'] = temp_user['last_name']
            temp['scores'] = score
            final.append(temp)
        return HttpResponse(json.dumps(final), content_type='application/json', status=200)


def submitScores(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        print("HELLO")
        course_id = str(request.POST.get('course_id'))
        scores = json.loads(request.POST.get('scores'))
        type_chosen = int(request.POST.get('type_chosen'))
        for score in scores:
            if int(scores[score]) == 0:
                continue
            upCond = dict()
            updateData = dict()
            updateData['scores'] = int(scores[score])
            if type_chosen == 1:
                updateData['status'] = "complete"
            upCond['$set'] = updateData

            checkData = dict()
            checkData['user_id'] = str(score)
            checkData['course_id'] = str(course_id)
            update_one("course_user", checkData, upCond)

        print(scores)
    return HttpResponse(json.dumps(list()), content_type='application/json', status=200)