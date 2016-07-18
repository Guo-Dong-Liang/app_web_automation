# coding=utf-8
from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template import RequestContext, Context, Template
from migu.models import *
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.core.mail import send_mail
import sys, time
import os
import subprocess
import datetime

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)


# Create your views here.
def login(request):
	# send_mail('Subject test', 'Here is the message.', '', ['dongliang.guo@outlook.com','dongliang.guo@h3c.com'],
	#           fail_silently=False)
	if request.user.is_authenticated():
		return render(request, 'home.html', {'username': request.user.username})
	else:
		return render_to_response('login.html')


def logout(request):
	if request.user.is_authenticated():
		auth.logout(request)
		return render_to_response('login.html')


def home(request):
	if request.user.is_authenticated():
		return render(request, 'home.html', {'username': request.user.username})
	else:
		return render_to_response('login.html')


def login_post(request):
	context_instance = RequestContext(request)
	context = {}
	username = None
	userpwd = None
	if request.POST:
		if not request.POST.get('username'):
			context['loginfail'] = 'Please Enter account'
			return render(request, "login.html", context)
		else:
			username = request.POST.get('username')
			context['username'] = username
		if not request.POST.get('password'):
			context['loginfail'] = 'Please Enter password'
			return render(request, "login.html", context)
		else:
			userpwd = request.POST.get('password')
		if username is not None and userpwd is not None:
			user = authenticate(username=username, password=userpwd)
			if user is not None:
				if user.is_active:
					auth.login(request, user)
					return render(request, 'home.html', context)
				else:
					context['loginfail'] = 'disabled account'
					return render(request, "login.html", context)
			else:
				context['loginfail'] = 'wrong password or user'
				return render(request, "login.html", context)


def youxi(request, tasktype):
	if request.user.is_authenticated():
		alltask = task.objects.filter(task_type=tasktype)
		taskrecord = task_record.objects.filter(task_record_user_id=request.user.id).order_by('-task_record_createtime')
		taskstatus = task_status.objects.all()
		return render(request, "youxi.html", {'tasks': alltask, 'taskstatus': taskstatus})
	else:
		return render_to_response('login.html')


def youxi_record(request, taskid):
	if request.user.is_authenticated():
		taskrecord = task_record.objects.filter(task_record_task_id=taskid).order_by('-task_record_createtime')[:10]
		return render(request, "taskrecord.html", {'taskrecord': taskrecord})
	else:
		return render_to_response('login.html')


def app_run(request, taskid):
	if request.user.is_authenticated():
		runtask = task.objects.get(pk=taskid)
		alltask = task.objects.filter(task_type=runtask.task_type)
		taskstatus = task_status.objects.all()

		# script.objects.get(pk=runtask.task_script_id_id)
		runscript = runtask.task_script_id
		repoteName = 'result_' + datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") + '.html'
		dirname = datetime.datetime.utcnow().strftime("%Y-%m-%d")
		# 生成测试报告文件
		reportpath = 'c:\\HistoryCheck\\GameApp\\%s\\Report\\%s' % (unicode(runtask.task_name), unicode(dirname))
		if not os.path.exists(reportpath):
			os.makedirs(reportpath)
		reportpath = os.path.join(reportpath, repoteName)

		starttaskcmd = 'python ' + runscript.script_path + ' ' + runscript.script_appiumport + ' ' + reportpath + ' ' + runscript.script_udid + ' ' + request.user.email + ' ' + taskid
		# 开始执行
		# runCmd('cmd /k appium')
		# subprocess.Popen('f:\\startAppium.bat', creationflags=subprocess.CREATE_NEW_CONSOLE)
		# time.sleep(10)
		runCmd(starttaskcmd)
		# 修改任务状态
		runtask.task_status = taskstatus.get(pk=2)
		runtask.save()
		# 开始添加执行记录
		newtaskrecord = task_record()
		newtaskrecord.task_record_task_id = runtask
		newtaskrecord.task_record_user_id = request.user
		newtaskrecord.task_record_status = taskstatus.get(pk=3)
		newtaskrecord.task_record_result_path = reportpath
		newtaskrecord.task_record_other = str(runscript.script_udid)
		newtaskrecord.save()
		taskrecord = task_record.objects.filter(task_record_user_id=request.user.id,
		                                        task_record_task_id=taskid).order_by('-task_record_createtime').first()
		return render(request, 'youxi.html', {'tasks': alltask, 'taskstatus': taskstatus, 'taskrecord': taskrecord})
	else:
		return render_to_response('login.html')


def download(request):
	try:
		def file_iterator(file_name, chunk_size=512):
			try:
				with open(file_name) as f:
					while True:
						c = f.read(chunk_size)
						if c:
							yield c
						else:
							break
			except:
				yield u"报告异常，暂时无法查看"

		if request.GET:
			filename = request.GET.get('dp')

		if os.path.basename(filename).endswith('html'):
			response = HttpResponse(file_iterator(filename))
		else:
			data_uri = open(filename, 'rb').read().encode('base64').replace('\n', '')
			response = '''
            <html>
            <head><title>图片详情</title></head>
            <body>
            <h1>请查看图片</h1>
            <img width='400px' src="data:image/jpg;base64,{0}" />
            </body>
            </html>
            '''.format(data_uri)
		return HttpResponse(response)
	except:
		return HttpResponse(u'报告不存在或者存在错误！')


# 定义执行cmd命令,默认打开新的窗口执行
def runCmd(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE):
	subprocess.Popen(cmd, creationflags=creationflags)
