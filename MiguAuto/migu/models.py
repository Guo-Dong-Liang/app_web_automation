# coding=utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin


# Create your models here.
# class AutoUser(models.Model):
#     username = models.CharField(max_length=100)
#     userpwd = models.CharField(max_length=100)
#     useremail = models.CharField(max_length=100)
#     userphone = models.CharField(max_length=100)
#     createdate = models.DateField(auto_now=True)
#
#     def __unicode__(self):
#         return self.username
class script(models.Model):
    script_path = models.CharField(u'脚本路径', max_length=100)
    script_name = models.CharField(u'脚本名称', max_length=100)
    script_description = models.CharField(u'脚本说明', max_length=100)
    script_createtime = models.DateTimeField(u'脚本创建时间', auto_now_add=True)
    script_appiumport = models.CharField(u'脚本服务端口', max_length=100, null=True)
    script_udid = models.CharField(u'执行设备标识', max_length=100, null=True)
    script_other = models.CharField(u'预留字段', max_length=100)

    class Meta:
        verbose_name = '脚本管理'
        verbose_name_plural = '脚本管理'

    def __unicode__(self):
        return self.script_name


# 脚本用例管理，我们采用unitest框架，一个脚本包含多个测试用例，这个模型用来管理脚本中的test
class script_test(models.Model):
    script_test_scriptid = models.ForeignKey(script, verbose_name=u'脚本名称')
    script_test_name = models.CharField(u'测试用例名称', max_length=100, unique=True)
    script_test_description = models.CharField(u'测试用例说明', max_length=300)
    script_test_createtime = models.DateTimeField(u'测试用例创建时间', auto_now=True)

    class Meta:
        verbose_name = '测试用例管理'
        verbose_name_plural = '测试用例管理'

    def __unicode__(self):
        return self.script_test_name


# 脚本参数管理，主要是准备后期在个人参数化时使用，当前不使用
class script_para(models.Model):
    script_para_scriptid = models.ForeignKey(script, verbose_name=u'和脚本关联的参数信息')
    script_para_userid = models.ForeignKey(User, verbose_name=u'和用户关联')
    script_para_key = models.CharField(u'脚本参数key值', max_length=100, unique=True)
    script_para_value = models.CharField(u'脚本参数value值', max_length=100)
    script_para_description = models.CharField(u'脚本参数说明', max_length=300)

    class Meta:
        verbose_name = '脚本参数管理'
        verbose_name_plural = '脚本参数管理'

    def __unicode__(self):
        return self.script_para_sriptid


class task_type(models.Model):
    task_type_typeid = models.IntegerField(u'任务类别id', primary_key=True, auto_created=True)
    task_type_description = models.CharField(u'任务类别说明', max_length=100)

    class Meta:
        verbose_name = '任务类别枚举值管理'
        verbose_name_plural = '任务类别枚举值管理'

    def __unicode__(self):
        return self.task_type_description


class task_status(models.Model):
    task_statusid = models.IntegerField(u'任务记录状态id', primary_key=True, auto_created=True)
    task_status_description = models.CharField(u'任务状态说明', max_length=100)

    class Meta:
        verbose_name = '任务状态枚举值管理'
        verbose_name_plural = '任务状态枚举值管理'

    def __unicode__(self):
        return self.task_status_description


class task(models.Model):
    task_name = models.CharField(u'任务名称', max_length=100)
    task_script_id = models.ForeignKey(script, verbose_name=u'任务对应的脚本')
    task_description = models.CharField(u'任务说明', max_length=300)
    task_type = models.ForeignKey(task_type, verbose_name=u'任务类别')
    task_createtime = models.DateTimeField(u'任务创建时间', auto_now=True)
    task_status = models.ForeignKey(task_status, verbose_name=u'任务状态')
    task_other = models.CharField(u'预留字段', max_length=100)

    class Meta:
        verbose_name = '任务管理'
        verbose_name_plural = '任务管理'

    def __unicode__(self):
        return self.task_name


class task_record(models.Model):
    task_record_task_id = models.ForeignKey(task, verbose_name=u'记录对应的任务')
    task_record_user_id = models.ForeignKey(User, verbose_name=u'记录对应的用户')
    task_record_status = models.ForeignKey(task_status, verbose_name=u'任务记录状态值')
    task_record_createtime = models.DateTimeField(u'任务记录创建时间', auto_now=True)
    task_record_result_path = models.CharField(u'任务结果记录路径', max_length=200)
    task_record_other = models.CharField(u'预留字段', max_length=100)

    class Meta:
        verbose_name = '任务历史管理'
        verbose_name_plural = '任务历史管理'

    def __unicode__(self):
        return str(self.task_record_task_id)
