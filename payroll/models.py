#coding=utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Employee_type(models.Model):
    employee_type_id=models.CharField(verbose_name=u"员工种类号",max_length=3,primary_key=True)
    employee_type=models.CharField(verbose_name=u"员工种类",max_length=20,unique=True)
    def __unicode__(self):
        return self.employee_type


class Department(models.Model):
    department_id=models.CharField(verbose_name=u"部门编号",max_length=3,primary_key=True)
    department_name=models.CharField(verbose_name=u"部门名称",max_length=20,unique=True)
    def __unicode__(self):
        return self.department_name


class Employee(User):
    sex_choices=(
        ('f','fmale'),
        ('m','male'),
    )
    sex = models.CharField(verbose_name=u'性别',max_length=1,choices=sex_choices,default='m')
    employee_type = models.ForeignKey('Employee_type')
    phone_number = models.CharField("phone_number",max_length=20)
    salary_rate = models.FloatField()
    department = models.ForeignKey('Department')
    def __unicode__(self):
        return self.name
    # 设置员工号为   部门号+员工种类+后续数字  的组合
    @property
    def employee_id(self):
        return "%s%s%s"%(self.department__id,self.employee_type__id,str(self.id))
    @property
    def name(self):
        return self.first_name + self.last_name
    # 创建员工后将员工数据插入到 登录验证表中
    def save(self,*args,**kwargs):
        super(Employee,self).save(*args,**kwargs)
    def create(self,*args,**kwargs):
        user=User.objects.create_user(username=self.employee_id , password='pknqaz12',email=self.email)
        user.set_password('pknqaz12')
        self.user_ptr_id=user.id
        super(User,self).create(*args,**kwargs)

