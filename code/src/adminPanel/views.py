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


