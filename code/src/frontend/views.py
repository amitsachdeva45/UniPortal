from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import pymongo
from .forms import SignUpForm
from university.common_function import get_id, insert_one
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



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