from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.cache import cache
from django.http import HttpResponseRedirect


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
    context['testing'] = "Ashu Singla"
    return render(request, "candidateCourse.html", context)




