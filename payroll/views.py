# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from payroll.models import *
import re
import datetime

emailRe = re.compile(r'^[\w\d]+[\w\d_\.]+@[\w\d]+\.[\w\d]+$')
phoneNumberRe = re.compile(r'^1\d{10}$')
bankCountRe = re.compile(r'^\d{16,19}$')


def home(request):
    post = Post.objects.all()[:15]
    notice =  Notice.objects.all()[:15]
    return render_to_response('payroll/home.html',{'login':False,'error':False,'post':post,'notice':notice})


def mylogin(request):
    errors = False
    loginSuccess = False
    post = Post.objects.all()[:15]
    notice =  Notice.objects.all()[:15]
    if request.method == 'POST':
        try:
            employeeId = request.POST['username']
            username = Employee.objects.get( employeeId=employeeId ).user.username
            password = request.POST['password']
        except Exception:
            errors = True
            return render_to_response('payroll/home.html',{'login':loginSuccess,'error':errors})
        user = authenticate( username = username ,password = password )
        if user is not None:
            if user.is_active:
                login(request,user)
                loginSuccess= True
            else:
                errors = True
                return render_to_response('payroll/home.html',{'login':loginSuccess,'error':errors})
        else:
            errors = True
            return render_to_response('payroll/home.html',{'login':loginSuccess,'error':errors})
    return render_to_response('payroll/home.html',{'login':loginSuccess,'error':errors,'post':post,'notice':notice})


def mylogout(request):
   logout(request) 
   return render_to_response('payroll/home.html',{'login':False,'error':False})


def person(request):
    user=request.user
    employee=user.employee
    if not user.is_authenticated():
        return render_to_response('payroll/home.html',{'login':False,'error':False})
    return render_to_response('payroll/person.html',{'login':True,'user':user,'employee':employee})


def maintainInfo(request):
    global phoneNumberRe
    global emailRe
    global bankCountRe
    errors=[False for i in range(5)]
    try:
        if request.method == 'POST':
            phoneNumber = request.POST['phoneNumber']
            bankCount =  request.POST['bankCount']
            email =  request.POST['email']
            sex = request.POST['sex']
            password0 =  request.POST['password0']
            password1 =  request.POST['password1']
            password2 = request.POST['password2']
            user = request.user
            if not user.is_authenticated():
                return render_to_response('payroll/home.html',{'login':False,'error':False})
            employee = user.employee
            if phoneNumber:
                if phoneNumberRe.match(phoneNumber) == None:
                    errors[0]=True
                else:
                    employee.phoneNumber = phoneNumber
                    employee.save()
            if bankCount:
                if bankCountRe.match(bankCount) == None:
                    errors[1] = True
                else:
                    employee.bankCount = bankCount
                    employee.save()
            if email:
                if emailRe.match(email) == None:
                    errors[2] = True
                else:
                    employee.email = email
                    employee.save()
            if sex == u'男':
                employee.sex='m'
                employee.save()
            else:
                employee.sex='f'
                employee.save()
            if password0 and password1 and password2:
                if password1 != password2:
                    errors[4]=True
                else:
                    username = user.username
                    password = password0
                    user = authenticate( username = username ,password = password )
                    if user is not None:
                        if user.is_active:
                            user.set_password(password1)
                            return render_to_response('payroll/person.html',{'login':True,'user':user,'employee':employee,'errors':errors,"changePassword":True})
                    else:
                        errors[3] = True
            elif password0 or password1 or password2:
                errors[4]=True
            return render_to_response('payroll/person.html',{'login':True,'user':user,'employee':employee,'errors':errors})
    except Exception:
        render_to_response('payroll/404.html')
    return render_to_response('payroll/404.html',{})


def aPost(request,id):
    try:
        id = int(id)
        thePost = Post.objects.get( pk=id )
        theComment = thePost.comment_set.all()
    except Exception:
        return render_to_response('payroll/404.html')
    return render_to_response('payroll/post.html',{'post':thePost,'comment':theComment})


def aNotice(request,id):
    try:
        id =  int(id)
        theNotice = Notice.objects.get( pk=id )
    except Exception:
        return render_to_response('payroll/404.html')
    return render_to_response('payroll/theNotice.html',{'notice':theNotice})


def allPost(request):
    post =  Post.objects.all()
    loginSuccess =  True
    user = request.user
    if not user.is_authenticated():
        loginSuccess = False
    return render_to_response('payroll/allPost.html',{'post':post,'login':loginSuccess})


def allNotice(request):
    notice =  Notice.objects.all()
    loginSuccess =  True
    try:
        user = request.user
        if not user.is_authenticated():
            loginSuccess = False
    except Exception:
        render_to_response('payroll/404.html')
    print notice
    return render_to_response('payroll/allNotice.html',{'notice':notice,'login':True})


def makeComment(request,id):
    if request.method == 'POST':
        try:
            id = int(id)
            user = request.user
            thePost = Post.objects.get( pk=id )
            print request.POST
            theComment = Comment.objects.create( content=request.POST['mycomment'],pubdate=datetime.datetime.now(),employee=user.employee,post=thePost )
            comments = thePost.comment_set.all()
        except Exception:
            return render_to_response('payroll/404.html')
    else:
        return render_to_response('payroll/404.html')
    return render_to_response('payroll/post',{'post':thePost,'comment':comments})
