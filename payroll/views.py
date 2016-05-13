from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

def home(request):
    return render_to_response('payroll/home.html',{})


def mylogin(request):
    logined=False
    if request.method == 'POST':
        un=request.POST['username']
        pwd=request.POST['password']
        user = authenticate(username=un,password=pwd)
        if user is not None:
            login(request,user)
            logined=True
    return render_to_response('payroll/home.html',{'login':logined})

def mylogout(request):
    pass
