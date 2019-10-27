from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CourseModelForm
from university.common_function import get_id, insert_one, get_all, get_find_one, update_one, delete_one
import json

# Create your views here.
def commonData():
    userData = cache.get("AdminData")
    if userData == None:
        return {}
    context = {
        "userDetail": userData,
        "userId": cache.get("AdminUserId"),
        "userName": userData['first_name'] + " " + userData['last_name']
    }
    return context

@login_required(login_url='/')
def adminHome(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    return render(request, "adminHome.html", context)


def fetchAllCourse():
    collections = "courses"
    return get_all(collections, {"id":{"$gt":1}}).sort("id",-1)

@login_required(login_url='/')
def adminCourse(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    form = CourseModelForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = dict()
            data['id'] = get_id("courses")
            data['course_name'] = request.POST.get('course_name')
            data['Description'] = request.POST.get('Description')
            data['branch_choice'] = request.POST.get('branch_choice')
            data['course_choice'] = request.POST.get('course_choice')
            data['semester'] = request.POST.get('semester')
            insert_one("courses", data)
            form = CourseModelForm(None)
    context['all_courses'] = fetchAllCourse()
    context['forms'] = form
    return render(request, "adminCourse.html", context)

@login_required(login_url='/')
def deleteCourse(request, id):
    data = dict()
    data['id'] = int(id)
    delete_one("courses", data)
    return HttpResponse(json.dumps(list()), content_type='application/json', status=200)


@login_required(login_url='/')
def fetchCandidate(request):
    context = commonData()
    if bool(context) != True:
        return HttpResponseRedirect("/")
    collections = "userBasicDetail"
    data = dict()
    data['type_of_user'] = "candidate"
    data['completion_status'] = "incomplete"
    results = get_all(collections, data)
    final_list = list()
    for result in results:
        data = dict()
        if result['branch_choice'] == "Bachelor":
            data['total_fees'] = 40000
        else:
            data['total_fees'] = 20000
        data['fees'] = result['fees']
        data['branch_choice'] = result['branch_choice']
        data['semester'] = result['current_semester']
        data['course_choice'] = result['course_choice']
        data['candidate_id'] = result['user_id']
        temp = dict()
        temp['id'] = result['user_id']
        cand = get_find_one("auth_user", temp)
        data['first_name'] = cand['first_name']
        data['last_name'] = cand['last_name']
        data['email'] = cand['email']
        final_list.append(data)
    context['candidates'] = final_list
    return render(request, "adminCandidate.html", context)
