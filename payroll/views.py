from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from payroll.models import Employee

def home(request):
    return render_to_response('payroll/home.html',{'login':False,'error':False})


def mylogin(request):
    errors = False
    loginSuccess = False
    if request.method == 'POST':
        employeeId = request.POST['username']
        em = Employee.objects.get( pk = 2 )
        u = em.user
        username = u.username
        # except Exception:
            # errors = True
            # print 'Exception'
        password = request.POST['password']
        user = authenticate( username = username ,password = password )
        if user is not None:
            if user.is_active:
                login(request,user)
                loginSuccess= True
            else:
                errors = True
        else:
            errors = True
    print 'errors',errors
    print 'login',loginSuccess
    return render_to_response('payroll/home.html',{'login':loginSuccess,'error':errors})


def mylogout(request):
   logout(request) 
   return render_to_response('payroll/home.html',{'login':False,'error':False})
