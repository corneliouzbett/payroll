#coding=utf8
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
from django.contrib import admin
from django.contrib.auth.views import login,logout
import payroll.views as payroll_view

admin.AdminSite.site_header=u'Payroll 系统管理'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$',payroll_view.home),
    url(r'^accounts/mylogin',payroll_view.mylogin),
    #url(r'^accounts/login',login,{'temlate_name':'home.html'}),
    url(r'^accounts/logout',logout,{'temlate_name':'home.html'}),
]
