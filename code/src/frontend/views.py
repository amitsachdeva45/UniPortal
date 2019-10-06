from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm, UserLoginForm
from university.common_function import get_id, insert_one, get_all, get_find_one
from datetime import date
from datetime import datetime
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect

User = get_user_model()

# @login_required(login_url='/')
# def tempview(request):
#     logout(request)
#     print("hello")
#     return render(request, "testing5.html", {})

def remainingSignup(form, id):
    obj = {}
    collection = "userBasicDetail"
    obj['user_id'] = id
    obj['date_of_birth'] = datetime.combine(form.cleaned_data.get('date_of_birth'), datetime.min.time())
    obj['semester_choice'] = form.cleaned_data.get('semester_choice')
    obj['branch_choice'] = form.cleaned_data.get('branch_choice')
    obj['course_choice'] = form.cleaned_data.get('course_choice')
    obj['type_of_user'] = form.cleaned_data.get('type_of_user')
    obj['starting_year'] = form.cleaned_data.get('starting_year')
    obj['completion_status'] = "incomplete"
    obj['current_semester'] = "1"
    insert_one(collection, obj)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=True)
            remainingSignup(form, obj.id)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'class': 'hiddenInputSignup'})



# def insert(request):
#     collection = 'notifications'
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             print("Haaaaaaa")
#             data_dict = {}
#             data_dict['id'] = get_id(collection)
#             data_dict['username'] = form.cleaned_data.get('username')
#             data_dict['last_name'] = form.cleaned_data['last_name']
#             data_dict['first_name'] = form.cleaned_data['first_name']
#             insert_one(collection, data_dict)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'home.html')
def fetchNotifications(is_public):
    collection = "notifications"
    data = dict()
    data['is_public'] = str(is_public)
    value = get_all(collection, data)
    notification = []
    for data1 in value:
        if data1['is_admin'] == "1":
            data1['name'] = "Admin"
        else:
            data2 = dict()
            data2['id'] = int(data1['user_id'])
            temp = get_find_one("auth_user", data2)
            name = temp['first_name'] + " "+ temp['last_name']
            data1['name'] = name
        notification.append(data1)
    return notification

def callAdmin(temp):
    print("Will Call admin")


def cachingData():
    cache_key = 'my_unique_key'  # needs to be unique
    cache_time = 86400  # time in seconds for cache to be valid
    data = cache.get(cache_key)  # returns None if no key-value pair
    if not data:
        cache.set(cache_key, data, cache_time)

def fetchUserDetail(request, email):
    collection = "auth_user"
    data = dict()
    data['email'] = email
    userData = get_find_one("auth_user", data)
    final_dict = dict()
    del userData['password']
    if userData['is_superuser'] == True:
        callAdmin(userData)
    else:
        data2 = dict()
        data2['user_id'] = int(userData['id'])
        remaining = get_find_one("userBasicDetail", data2)
        userData.update(remaining)
        if remaining['type_of_user'] == "candidate":
            cache.set("CandidateData", userData)
            cache.set("CandidateUserId", userData['id'])
            return "candidate"
        else:
            print("Will Call teacher page")




def home(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    context = {
        "form": form,
        "notifications": fetchNotifications(1)
    }
    if form.is_valid():
        email = form.cleaned_data.get('email')
        user_obj = User.objects.get(email__iexact = email)
        login(request,user_obj)
        response = fetchUserDetail(request, email)
        if response == "candidate":
            return redirect("candidate:candidateHome")
    return render(request, "home.html", context)


def logoutHome(request):
    logout(request)
    cache.clear()
    return HttpResponseRedirect("/")
