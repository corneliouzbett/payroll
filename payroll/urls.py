#coding=utf-8
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
import payroll.views as payroll_view

urlpatterns = [
    url(r'^person([1-4]{1})',payroll_view.person,name='person'),
    url(r'^home',payroll_view.home,name='home'),
    url(r'^login',payroll_view.mylogin,name='login'),
    url(r'^logout',payroll_view.mylogout,name='logout'),
    url(r'^maintainInfo',payroll_view.maintainInfo,name='maintainInfo'),
    url(r'^post([0-9]+)',payroll_view.aPost,name="post"),
    url(r'^notice([0-9]+)',payroll_view.aNotice,name="notice"),
    url(r'^allPost',payroll_view.allPost,name='allPost'),
    url(r'^allNotice',payroll_view.allNotice,name='allNotice'),
    url(r'^makeComment([0-9]+)',payroll_view.makeComment,name='makeComment'),
    url(r'^attend',payroll_view.attend,name='attend'),
    url(r'^makePost',payroll_view.makePost,name='makePost'),
    url(r'^getPayroll',payroll_view.getPayroll,name='getPayroll'),
]
