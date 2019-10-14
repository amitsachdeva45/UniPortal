from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.cache import cache
from datetime import datetime
from university.common_function import get_id, insert_one, get_all, get_find_one, update_one
from django.http import HttpResponseRedirect, HttpResponse
import json
from .forms import PostModelForm

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
    data['status'] = "incomplete"
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


def updateTeacherCourseStatus(course_id):
    upCond = dict()
    updateData = dict()
    updateData['status'] = "complete"
    upCond['$set'] = updateData
    checkData = dict()
    checkData['user_id'] = str(cache.get("TeacherUserId"))
    checkData['course_id'] = str(course_id)
    update_one("course_teacher", checkData, upCond)

def submitScores(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    if request.method == "POST":
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
                updateTeacherCourseStatus(course_id)
            upCond['$set'] = updateData

            checkData = dict()
            checkData['user_id'] = str(score)
            checkData['course_id'] = str(course_id)
            update_one("course_user", checkData, upCond)
    return HttpResponse(json.dumps(list()), content_type='application/json', status=200)

def fetchNotification():
    collection = "notifications"
    data = dict()
    data['user_id'] = str(cache.get("TeacherUserId"))
    final_dict = dict()
    final_dict['$query'] = data
    final_dict['$orderby'] = {"date_posted": -1}
    value = get_all(collection, final_dict)
    return value

@login_required(login_url='/')
def teacherNotification(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    form = PostModelForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            notification = dict()
            notification['degree'] = request.POST.get('degree')
            notification['course'] = request.POST.get('course')
            notification['description'] = request.POST.get('description')
            notification['date_posted'] = datetime.now()
            notification['is_public'] = str(request.POST.get('public'))
            notification['is_admin'] = "0"
            notification['user_id'] = str(cache.get("TeacherUserId"))
            insert_one("notifications", notification)
            form = PostModelForm(None)
    context['forms'] = form
    context['notifications'] = fetchNotification()
    return render(request, "teacherNotification.html", context)