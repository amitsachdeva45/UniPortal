from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import pymongo
from .forms import SignUpForm
from university.common_function import get_id, insert_one
from datetime import date
from datetime import datetime


def remainingSignup(form, id):
    obj = {}
    collection = "userBasicDetail"
    obj['user_id'] = id
    obj['date_of_birth'] = datetime.combine(form.cleaned_data.get('date_of_birth'), datetime.min.time())
    obj['semester_choice'] = form.cleaned_data.get('semester_choice')
    obj['branch_choice'] = form.cleaned_data.get('branch_choice')
    obj['type_of_user'] = form.cleaned_data.get('type_of_user')
    obj['starting_year'] = form.cleaned_data.get('starting_year')
    insert_one(collection, obj)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=True)
            remainingSignup(form, obj.id)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'class': 'hiddenInputSignup'})



def insert(request):
    collection = 'notifications'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("Haaaaaaa")
            data_dict = {}
            data_dict['id'] = get_id(collection)
            data_dict['username'] = form.cleaned_data.get('username')
            data_dict['last_name'] = form.cleaned_data['last_name']
            data_dict['first_name'] = form.cleaned_data['first_name']
            insert_one(collection, data_dict)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})