#coding=utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class EmployeeType(models.Model):
    name = models.CharField( verbose_name="员工种类", max_length=20, unique=True )
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
    phoneNumber = models.CharField( "手机号",max_length=20 )
    salaryPerHour = models.FloatField()
    employeeId = models.CharField(max_length=20,null=True,unique=True)
    department = models.ForeignKey( 'Department' )
    def __unicode__(self):
        return self.name
    # 设置员工号为   部门号+员工种类+后续数字  的组合
    def save(self,*args,**kwargs):
        departmentId = unicode(self.department_id)
        departmentId = u'0'+departmentId if len(departmentId)<2 else departmentId
        typeId = unicode(self.type_id)
        typeId = u'0'+typeId if len(typeId)<2 else typeId
        sid = unicode(self.id)
        sid = u'0'*(4-len(sid))+sid if len(sid)<4 else sid
        self.employeeId=u"%s%s%s"%(departmentId,typeId,sid)
        super(Employee,self).save(*args,**kwargs)

    def create(self,*args,**kwargs):
        departmentId = unicode(self.department_id)
        departmentId = u'0'+departmentId if len(departmentId)<2 else departmentId
        typeId = unicode(self.type_id)
        typeId = u'0'+typeId if len(typeId)<2 else typeId
        sid = unicode(self.id)
        sid = u'0'*(4-len(sid))+sid if len(sid)<4 else sid
        self.employeeId=u"%s%s%s"%(departmentId,typeId,sid)
        super(Employee,self).create(*args,**kwargs)

