from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
import json
from university.common_function import get_id, insert_one, get_all, get_find_one

def commonData():
    userData = cache.get("CandidateData")
    if userData == None:
        return False
    total_semester = 4
    if userData['branch_choice'] == 'Master':
        total_semester = 4
    else:
        total_semester = 8
    current_semester = int(userData['current_semester'])
    if userData == None:
        return {}
    context = {
        "userDetail": userData,
        "userId": cache.get("CandidateUserId"),
        "userName": userData['first_name'] + " " + userData['last_name'],
        "total_semester": range(1, total_semester+1),
        "remaining_semester": range(current_semester, total_semester+1)
    }
    return context

@login_required(login_url='/')
def candidateHome(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    return render(request, "candidateHome.html", context)

@login_required(login_url='/')
def candidateCourse(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    #context['tempData'] = json.loads(candidateFetchCourse(request).content)
    return render(request, "candidateCourse.html", context)

@login_required(login_url='/')
def candidateFetchCourse(request):
    data2 = dict()
    data2['user_id'] = str(cache.get("CandidateUserId"))
    all_courses = get_all("course_user", data2)
    data = list()
    for course in all_courses:
        temp = list()
        data2 = dict()
        data2['semester'] = str(request.POST.get('semester'))
        data2['id'] = int(course['course_id'])
        single_course = get_find_one("courses", data2)
        if single_course != None:
            data2['status'] = course['status']
            data2['course_name'] = single_course['course_name']
            data2['description'] = single_course['Description']
            data2['branch_choice'] = single_course['branch_choice']
            data2['course_choice'] = single_course['course_choice']
            data.append(data2)
    return HttpResponse(json.dumps( data ), content_type='application/json', status=200)


@login_required(login_url='/')
def candidateFetchEachSemCourse(request, id):
    data2 = dict()
    userData = cache.get("CandidateData")
    data2['semester'] = str(id)
    data2['course_choice'] = str(userData['course_choice'])
    data2['branch_choice'] = str(userData['branch_choice'])
    all_courses = get_all("courses", data2)
    data = list()
    for course in all_courses:
        temp = dict()
        data2 = dict()
        data2['user_id'] = str(userData['id'])
        data2['course_id'] = str(course['id'])
        single_course = get_find_one("course_user", data2)
        if single_course == None:
            temp['id'] = str(course['id'])
            temp['user_id'] = str(userData['id'])
            temp['name'] = course['course_name']
            temp['semester'] = str(id)
            temp['description'] = course['Description']
            data.append(temp)
    return HttpResponse(json.dumps(data), content_type='application/json', status=200)


def selectCourse(request):
    semester = "-1"

    if request.method == 'POST':
        data = dict()
        data['course_id'] = str(request.POST.get('course_id'))
        data['user_id'] = str(request.POST.get('user_id'))
        data['status'] = "incomplete"
        insert_one("course_user", data)
        return HttpResponse(json.dumps(list()), content_type='application/json', status=200)
    return HttpResponse(json.dumps(list()), content_type='application/json', status=404)

@login_required(login_url='/')
def fetchNotification(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    collection = "notifications"
    userData = cache.get("CandidateData")
    data = dict()
    data['is_public'] = "0"
    data['degree'] = str(userData['branch_choice'])
    data['course'] = str(userData['course_choice'])
    final_dict = dict()
    final_dict['$query'] = data
    final_dict['$orderby'] = {"date_posted": -1}
    value = get_all(collection, final_dict)
    notification = []
    for data1 in value:
        if data1['is_admin'] == "1":
            data1['name'] = "Admin"
        else:
            data2 = dict()
            data2['id'] = int(data1['user_id'])
            temp = get_find_one("auth_user", data2)
            name = temp['first_name'] + " " + temp['last_name']
            data1['name'] = name
        notification.append(data1)
    context['notifications'] = notification
    return render(request, "candidateNotification.html", context)