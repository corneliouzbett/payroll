# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db.models import Sum
from payroll.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    user = request.user
    employee = user.employee
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
    user = request.user
    employee = user.employee
    myPost = Post.objects.filter(employee=employee)
    tmpComment = Comment.objects.filter(employee=employee)
    tmpId = []
    myComment = []
    for item in tmpComment:
        if item.post.id not in tmpId:
            tmpId.append(item.post.id)
            myComment.append(item)
    # try:
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
                        return render_to_response('payroll/person.html',{'login':True,'user':user,'employee':employee,'errors':errors,"changePassword":True,'myPost':myPost,'myComment':myComment})
                else:
                    errors[3] = True
        elif password0 or password1 or password2:
            errors[4]=True
        return render_to_response('payroll/person.html',{'login':True,'user':user,'employee':employee,'errors':errors,'myComment':myComment,'myPost':myPost})
    # except Exception:
        # render_to_response('payroll/404.html')
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
    paginator = Paginator(post,10)
    num_pages =  paginator.num_pages
    try:
        pagenum = int(request.GET.get('page','1'))
    except ValueError:
        pagenum = 1
    data = paginator.page(pagenum)
    return render_to_response('payroll/allPost.html',{'post':data,'login':loginSuccess,'num_pages':num_pages})


@login_required(login_url='/payroll/home')
def allNotice(request):
    notice =  Notice.objects.all()
    return render_to_response('payroll/allNotice.html',{'notice':notice,'login':True})


@login_required(login_url='/payroll/home')
def makeComment(request,id):
    if request.method == 'POST':
        id = int(id)
        user = request.user
        thePost = Post.objects.get( pk=id )
        thePost.modifyDateTime = datetime.now()
        thePost.save()
        print request.POST
        theComment = Comment.objects.create( content=request.POST['mycomment'],pubdate=datetime.now(),employee=user.employee,post=thePost )
        comments = thePost.comment_set.all()
    else:
        return render_to_response('payroll/404.html')
    return render_to_response('payroll/post.html',{'post':thePost,'comment':comments,'login':True})

@login_required(login_url='/payroll/home')
def attend(request):
    if request.method == 'POST':
        user = request.user  
        employee = user.employee
        myPost = Post.objects.filter(employee=employee)
        tmpComment = Comment.objects.filter(employee=employee)
        tmpId = []
        myComment = []
        for item in tmpComment:
            if item.post.id not in tmpId:
                tmpId.append(item.post.id)
                myComment.append(item)
        st = request.POST['from1'].split('-')
        et = request.POST['to1'].split('-')
        recordTable = AttendRecord.objects.filter( employee=user.employee ).filter( date__gte = datetime(int(st[0]),int(st[1]),int(st[2])) ).filter( date__lte = datetime(int(et[0]),int(et[1]),int(et[2])) ).order_by('date')
        return render_to_response('payroll/person.html',{'login':True,'user':user,'employee':user.employee,'record':recordTable,'num':1,'myPost':myPost,'myComment':myComment})
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


@login_required(login_url='/payroll/home')
def getPayroll(request):
    if request.method == 'POST':
        dateFrom = request.POST['from2'].split('-')
        dateTo =  request.POST['to2'].split('-')
        yearFrom = int(dateFrom[0])
        monthFrom = int(dateFrom[1])
        yearTo = int(dateTo[0])
        monthTo = int(dateTo[1])
        if yearFrom*12 + monthFrom <= yearTo*12 + monthTo:
            # report = Payroll.objects.filter(employee=request.user.employee).filter( yearFrom*12+monthFrom <= year*12+month ).filter(year*12+month <= yearTo*12+monthTo)
            report = Payroll.objects.raw('''
                                         select * from payroll_payroll
                                         where %s+%s <= year*12+month and 
                                               year*12+month <= %s*12+%s and employee_id=%s
                                         ''',[yearFrom*12,monthFrom,yearTo*12,monthTo,request.user.employee.id])
            employee = request.user.employee
            myPost = Post.objects.filter(employee=employee)
            tmpComment = Comment.objects.filter(employee=employee)
            tmpId = []
            myComment = []
            for item in tmpComment:
                if item.post.id not in tmpId:
                    tmpId.append(item.post.id)
                    myComment.append(item)
            return render_to_response('payroll/person.html',{'login':True,'user':request.user,'employee':\
                                request.user.employee,'num':2,'myPost':myPost,'myComment':myComment,'report':report})
    else:
        return render_to_response('payroll/404.html')



def adminLogin(request):
    return render_to_response('payroll/adminLogin.html')



def adlogin(request):
    errors = False
    loginSuccess = False
    if request.method == 'POST':
        try:
            password = request.POST['password']
        except Exception:
            errors = True
            return render_to_response('payroll/adminLogin.html',{'login':loginSuccess,'error':errors})
        user = authenticate( username = 'admin' ,password = password )
        if user is not None:
            if user.is_active:
                login(request,user)
                loginSuccess= True
            else:
                errors = True
                return render_to_response('payroll/adminLogin.html',{'login':loginSuccess,'error':errors})
        else:
            errors = True
            return render_to_response('payroll/adminLogin.html',{'login':loginSuccess,'error':errors})
    return render_to_response('payroll/adminLogin.html',{'login':loginSuccess,'error':errors})



def adlogout(request):
   logout(request) 
   return render_to_response('payroll/adminLogin.html',{'login':False,'error':False})
   

@login_required(login_url='/payroll/adminLogin')
def makeReport(request):
    month = request.POST['month']
    year = request.POST['year']
    payroll = Payroll.objects.filter( year=year ).filter(month=month)
    hour = 0.0
    salary = 0.0
    num = len(payroll)
    for item in payroll:
        hour+=item.hour
        salary+=item.salary
    print hour,salary,num
    return render_to_response('payroll/adminreport.html',{'payroll':payroll,'num':num,'month':month,'year':year,'hour':hour,'salary':salary,'avgsalary':salary/num,'avghour':float("%.1f"%(hour/num/30.0,))})
