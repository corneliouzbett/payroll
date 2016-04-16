from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Books

def hello(request):
    return HttpResponse('hello world')

def showbooks(request):
	books=Books.objects.all()
	return render_to_response('book.html',locals())
