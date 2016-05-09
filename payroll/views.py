from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate,login

def home(request):
    return render_to_response('payroll/home.html',{})

def mylogin(request):
    login=False
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            login=True

    else:
        return render_to_response('payroll/home.html',{'login':login},context_instance=RequestContext(request))

def mylogout(request):
    pass
