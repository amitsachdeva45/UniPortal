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
        return {}
    context = {
        "userDetail": userData,
        "userId": cache.get("CandidateUserId"),
        "userName": userData['first_name'] + " " + userData['last_name'],
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







