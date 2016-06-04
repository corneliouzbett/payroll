#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import time
from django.core.mail import send_mail


class EmployeeType(models.Model):
    name = models.CharField( verbose_name="员工种类", max_length=20, unique=True )
    salaryPerHour = models.FloatField( "时薪" ) 
    def __unicode__(self):
        return self.name


class Department(models.Model):
    name = models.CharField( verbose_name="部门名称", max_length=20, unique=True )
    def __unicode__(self):
        return self.name


class Employee(models.Model):
    sex_choices=(
        ('f','女'),
        ('m','男'),
    )
    user = models.OneToOneField( User )
    name =  models.CharField( max_length=20 )
    sex = models.CharField( verbose_name='性别',max_length=1,choices=sex_choices,default='m' )
    type = models.ForeignKey( 'EmployeeType' )
    phoneNumber = models.CharField( "手机号",max_length=20,null=True )
    employeeId = models.CharField(blank=True,max_length=20,null=True,unique=True)
    department = models.ForeignKey( 'Department' )
    email =  models.EmailField(null=True)
    bankCount = models.CharField( max_length=20 )
    def __unicode__(self):
        return self.name
    # 设置员工号为   部门号+员工种类+后续数字  的组合
    def save(self,*args,**kwargs):
        super(Employee,self).save(*args,**kwargs)
        departmentId = unicode(self.department_id)
        departmentId = u'0'+departmentId if len(departmentId)<2 else departmentId
        typeId = unicode(self.type_id)
        typeId = u'0'+typeId if len(typeId)<2 else typeId
        sid = unicode(self.id)
        sid = u'0'*(4-len(sid))+sid if len(sid)<4 else sid
        self.employeeId=u"%s%s%s"%(departmentId,typeId,sid)
        super(Employee,self).save(*args,**kwargs)

    def create(self,*args,**kwargs):
        super(Employee,self).create(*args,**kwargs)
        departmentId = unicode(self.department_id)
        departmentId = u'0'+departmentId if len(departmentId)<2 else departmentId
        typeId = unicode(self.type_id)
        typeId = u'0'+typeId if len(typeId)<2 else typeId
        sid = unicode(self.id)
        sid = u'0'*(4-len(sid))+sid if len(sid)<4 else sid
        self.employeeId=u"%s%s%s"%(departmentId,typeId,sid)
        super(Employee,self).save(*args,**kwargs)



class AttendRecord(models.Model):
    date=models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    hour = models.FloatField(null=True,blank=True)
    employee = models.ForeignKey( 'Employee' )
    def __unicode__(self):
        return unicode(self.employee)+" "+unicode(self.date)
    def save(self,*args,**kwargs):
        super(AttendRecord,self).save(*args,**kwargs)
        self.hour = (self.end.hour*60.0 + self.end.minute*1.0 - self.start.hour*60.0 - self.start.minute*1.0)/60.0
        self.hour = float("%.1f"%(self.hour,))
        super(AttendRecord,self).save(*args,**kwargs)
    def create(self,*args,**kwargs):
        super(AttendRecord,self).create(*args,**kwargs)
        self.hour = (self.end.hour*60.0 + self.end.minute*1.0 - self.start.hour*60.0 - self.start.minute*1.0)/60.0
        self.hour = float("%.1f"%(self.hour,))
        super(AttendRecord,self).create(*args,**kwargs)


class Notice(models.Model):
    title =  models.CharField(max_length=255)
    content = models.TextField()
    pubdate = models.DateField(auto_now=True)
    def __unicode__(self):
        return unicode(self.title)
    

class Post(models.Model):
    title =  models.CharField(max_length=255)
    content = models.TextField()
    pubdate = models.DateField(auto_now=True)
    employee = models.ForeignKey('Employee')
    modifyDateTime = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-modifyDateTime']
    def __unicode__(self):
        return unicode(self.title)


class Comment(models.Model):
    pubdate = models.DateField(auto_now=True)
    content = models.TextField()
    employee = models.ForeignKey( 'Employee' )
    post = models.ForeignKey( 'Post' )
    def __unicode__(self):
        return unicode(self.employee) 
    


class Payroll(models.Model):
    employee = models.ForeignKey('Employee')
    year = models.IntegerField()
    month = models.IntegerField()
    employeeType = models.ForeignKey('EmployeeType')
    hour = models.IntegerField()
    salary = models.FloatField()
    def save(self,*args,**kwargs):
        super(Payroll,self).save(*args,**kwargs)
        subject = u'工资单'
        message = u'''
                        %s 您好！您本月共工作 %f 小时，应领取工资 %f 元，工资已经发送到您预留的银行账户 %s 中，请注意查收。
                        您也可以登录公司管理系统，在个人页面中核对本月的详细工作记录。
                        '''%(self.employee.name, self.hour, self.employee.bankCount)
        send_mail(subject, message, EMAIL_HOST_USER, self.employee.email, fail_silently=False)
