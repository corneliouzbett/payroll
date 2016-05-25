# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from payroll.models import *
import re
from datetime import datetime

emailRe = re.compile(r'^[\w\d]+[\w\d_\.]+@[\w\d]+\.[\w\d]+$')
phoneNumberRe = re.compile(r'^1\d{10}$')
bankCountRe = re.compile(r'^\d{16,19}$')


def home(request):
    post = Post.objects.all()[:15]
    notice =  Notice.objects.all()[:15]
    try:
        user = request.user
        if user is not None:
            return render_to_response('payroll/home.html',{'login':True,'error':False,'post':post,'notice':notice})
    except Exception:
        return render_to_response('payroll/home.html',{'login':False,'error':False,'post':post,'notice':notice})
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


@login_required(login_url='/payroll/home')
def person(request,id):
    id = int(id)
    user=request.user
    employee=user.employee
    myPost = Post.objects.filter(employee=employee)
    tmpComment = Comment.objects.filter(employee=employee)
    tmpId = []
    myComment = []
    for item in tmpComment:
        if item.post.id not in tmpId:
            tmpId.append(item.post.id)
            myComment.append(item)
    if not user.is_authenticated():
        return render_to_response('payroll/home.html',{'login':False,'error':False})
    return render_to_response('payroll/person.html',{'login':True,'user':user,'employee':employee,'num':id-1,'myPost':\
                                                     myPost,'myComment':myComment})


@login_required(login_url='/payroll/home')
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


@login_required(login_url='/payroll/home')
def aPost(request,id):
    try:
        id = int(id)
        thePost = Post.objects.get( pk=id )
        theComment = thePost.comment_set.all()
    except Exception:
        return render_to_response('payroll/404.html')
    return render_to_response('payroll/post.html',{'post':thePost,'comment':theComment,'login':True})


@login_required(login_url='/payroll/home')
def aNotice(request,id):
    try:
        id =  int(id)
        theNotice = Notice.objects.get( pk=id )
    except Exception:
        return render_to_response('payroll/404.html')
    return render_to_response('payroll/theNotice.html',{'notice':theNotice,'login':True})


@login_required(login_url='/payroll/home')
def allPost(request):
    post =  Post.objects.all()
    loginSuccess =  True
    user = request.user
    if not user.is_authenticated():
        loginSuccess = False
    return render_to_response('payroll/allPost.html',{'post':post,'login':loginSuccess})


@login_required(login_url='/payroll/home')
def allNotice(request):
    notice =  Notice.objects.all()
    return render_to_response('payroll/allNotice.html',{'notice':notice,'login':True})


@login_required(login_url='/payroll/home')
def makeComment(request,id):
    if request.method == 'POST':
        try:
            id = int(id)
            user = request.user
            thePost = Post.objects.get( pk=id )
            thePost.modifyDateTime =  datetime.datetime.now()
            thePost.save()
            print request.POST
            theComment = Comment.objects.create( content=request.POST['mycomment'],pubdate=datetime.datetime.now(),employee=user.employee,post=thePost )
            comments = thePost.comment_set.all()
        except Exception:
            return render_to_response('payroll/404.html')
    else:
        return render_to_response('payroll/404.html')
    return render_to_response('payroll/post.html',{'post':thePost,'comment':comments})

@login_required(login_url='/payroll/home')
def attend(request):
    if request.method == 'POST':
        # try:
            print request.POST
            st = request.POST['from1'].split('-')
            et = request.POST['to1'].split('-')
            user = request.user  
            recordTable = AttendRecord.objects.filter( employee=user.employee ).filter( date__gte = datetime(int(st[0]),int(st[1]),int(st[2])) ).filter( date__lte = datetime(int(et[0]),int(et[1]),int(et[2])) ).order_by('date')
            print recordTable
        # except Exception:
            # return render_to_response('payroll/404.html')
            return render_to_response('payroll/person.html',{'login':True,'user':user,'employee':user.employee,'record':recordTable,'num':1})
    else:
        return render_to_response('payroll/404.html',)


@login_required(login_url='/payroll/home')
def makePost(request):
    postTitle = request.POST['postTitle']
    postContent = request.POST['postContent']
    user =  request.user
    Post.objects.create( title=postTitle,content=postContent,employee=user.employee )
    post = Post.objects.all()
    return render_to_response('payroll/allPost.html',{'post':post,'login':True})
