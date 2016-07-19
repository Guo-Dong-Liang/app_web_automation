# -*- coding: UTF-8 -*-
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import sqlite3
import email
import smtplib
import re
import os
import time
import subprocess
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from selenium.common.exceptions import *
# 公共配置项，SQLITE_PATH表示数据库的路径，这里使用sqlite3
SQLITE_PATH = 'C:\MiguAuto\db.sqlite3'
mail_host = "smtp.139.com"
mail_user = "gamecenter@139.com"
mail_pass = "jiangsumobile"


class runUser:
    '''this is a doc'''
    # 初始化时候把参数带进来 调用时：python xxx.py  para1 para2 para3 para4 ...
    # 第一个参数默认是脚本的名称，在第0个位置
    # 第二个参数，在第1个位置，这里和框架约定为监听的appium服务端口号
    # 第三个参数，在第2个位置，表示存储结果报告的路径
    # 第四个参数，表示运行手机设备的唯一id
    # 第五个参数，表示登录框架的测试用户的邮箱
    # 第六个参数，表示当前运行的任务的id，可以用来更新任务的状态和做其他操作
    def __init__(self, para, apppackage, appactivity):
        try:
            if len(para) > 1:
                self.port = para[1]
            else:
                self.port = '4723'
            if len(para) > 2:
                self.resultpath = para[2].decode()
            else:
                self.resultpath = 'c:\\HistoryCheck\\GameApp\\YouXi\\Report\\temp_result.html'
            if len(para) > 3:
                self.udid = para[3]
            else:
                self.udid = 'bf452a70'
            if len(para) > 4:
                self.useremail = para[4]
            else:
                self.useremail = 'smoontar@qq.com'
            if len(para) > 5:
                self.taskid = para[5]
            else:
                self.taskid = 0
            # 把driver在初始化的时候传递过来
            self.driver = self.startApp(apppackage, appactivity)
        except Exception, e:
            print str(e)

    # 判断appium是否启动成功，如果存在监听端口则返回true否则返回false
    def ifAppiumRunning(self):
        checkAppium = subprocess.Popen('cmd /c netstat -ano|findstr ' + self.port,
                                       creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.PIPE)
        AppiumStat = checkAppium.communicate()[0]
        if self.port in AppiumStat:
            if 'LISTENING' in AppiumStat:
                print 'appium is already runing!'
                return True
            else:
                return False
        else:
            return False

    # 启动appium，使用命令行进行启动
    def startAppium(self):
        self.runCmd('cmd /k appium ' + '-p ' + self.port)
        self.waitForRunning()

    # 在新的窗口启动命令
    def runCmd(self, cmd, creationflags=subprocess.CREATE_NEW_CONSOLE):
        subprocess.Popen(cmd, creationflags=creationflags)

    # 等待appium服务启动，最多等待1分钟
    def waitForRunning(self):
        now = datetime.datetime.now()
        while not self.ifAppiumRunning():
            time.sleep(5)
            tl = datetime.datetime.now() - now
            # 如果1分钟还是没有启动appium就退出
            if tl.seconds > 60:
                print u'appium服务启动失败！'
                break

    # driver表示远程连接的控制器，str_desc表示你要保存图片的名字
    def saveRightImg(self, str_desc, driver=None):
        if driver is None:
            driver = self.driver
        rightscreenshotname = time.strftime('%Y-%m-%d_%H%M%S')
        rightPath = time.strftime('%Y-%m-%d')
        rightscreenshotpath = os.path.dirname(os.path.dirname(os.path.dirname(self.resultpath)))
        rightscreenshotpath = os.path.join(rightscreenshotpath, 'rightImg')
        rightscreenshotpath = os.path.join(rightscreenshotpath, rightPath)
        if not os.path.exists(rightscreenshotpath):
            os.makedirs(rightscreenshotpath)
        rightscreenshotpath = os.path.join(rightscreenshotpath,
                                           str_desc.replace(':', '_') + rightscreenshotname + '.png')
        rightscreenshotpath = unicode(rightscreenshotpath)
        # 打印截图的信息，让htmltestrunner获取截图地址
        print "image:%s" % '/download?dp='+rightscreenshotpath
        driver.get_screenshot_as_file(rightscreenshotpath)

    # driver表示远程连接的控制器，str_desc表示你要保存图片的名字
    def saveErrorImg(self, str_desc, driver=None):
        if driver is None:
            driver = self.driver
        errorscreenshotname = time.strftime('%Y-%m-%d_%H%M%S')
        errorPath = time.strftime('%Y-%m-%d')
        errorscreenshotpath = os.path.dirname(os.path.dirname(os.path.dirname(self.resultpath)))
        errorscreenshotpath = os.path.join(errorscreenshotpath, 'ErrorImg')
        errorscreenshotpath = os.path.join(errorscreenshotpath, errorPath)
        if not os.path.exists(errorscreenshotpath):
            os.makedirs(errorscreenshotpath)
        errorscreenshotpath = os.path.join(errorscreenshotpath,
                                           str_desc.replace(':', '_') + errorscreenshotname + '.png')
        errorscreenshotpath = unicode(errorscreenshotpath)
        # 打印截图的信息，让htmltestrunner获取截图地址
        print "image:%s" % '/download?dp='+errorscreenshotpath
        driver.get_screenshot_as_file(errorscreenshotpath)

    # desired_caps['appWaitActivity']= '.activity.root.TournamentList',启动app开始测试
    def startApp(self, apppackage, appactivity, udid=None, appiumaddress=None):
        if udid is None:
            udid = self.udid
        if appiumaddress is None:
            appiumaddress = 'localhost:' + self.port
        # 启动app之前要先判断appium是否启动
        if self.ifAppiumRunning():
            print 'appium is already running,we can use it!'
        else:
            self.startAppium()
            self.waitForRunning()
        phone_dec = {'device': 'android', 'platformName': 'Android', 'version': '4.4.2', 'udid': udid,
                     'deviceName': 'migu',
                     'appPackage': apppackage, 'appActivity': appactivity, 'unicodeKeyboard': True,
                     'resetKeyboard': True}
        try:
            app = webdriver.Remote("http://" + appiumaddress + "/wd/hub", phone_dec)
            return app
        except Exception, e:
            self.updatebysql('update migu_task set task_status_id=4 where id=' + str(self.taskid))
            self.sendemail(u'启动游戏应用报错', u'你好<br />请查看服务器是否运行正常,尝试重新执行任务<br />错误信息:' + str(e), self.useremail,
                           'dongliang.guo@h3c.com')

    # 执行sql语句
    # canrun----可执行
    # runfail----执行失败
    # runbreak----执行中断
    # running----执行中
    def updatebysql(self, sql, status=None, sqlitepaht=SQLITE_PATH):
        try:
            if status is not None:
                if status == 'canrun':
                    sql = 'update migu_task set task_status_id=1 where id=' + str(self.taskid)
                if status == 'runfail':
                    sql = 'update migu_task set task_status_id=4 where id=' + str(self.taskid)
                if status == 'runbreak':
                    sql = 'update migu_task set task_status_id=3 where id=' + str(self.taskid)
                if status == 'running':
                    sql = 'update migu_task set task_status_id=2 where id=' + str(self.taskid)
            else:
                pass
            cx = sqlite3.connect(sqlitepaht)
            cu = cx.cursor()
            cu.execute(sql)
            cx.commit()
            cx.close()
        except Exception, e:
            self.sendemail(u'更新数据库失败', u'你好<br />请查看服务器是否运行正常,尝试重新执行任务<br />错误信息:' + str(e), self.useremail,
                           'dongliang.guo@h3c.com')

    # 发送邮件,如果要发送多个人，直接a@h3c.com;b@h3c.com;c@h3c.com
    def sendemail(self, subject, body, mailto_list=None, mailcc='smoontar@qq.com', mailatt=None):
        if mailto_list is None:
            mailto_list = self.useremail
        mail_postfix = "migu.com"
        msg = MIMEMultipart()
        mailbody = MIMEText(body, 'html', 'gb2312')
        msg.attach(mailbody)
        if mailatt:
            att1 = MIMEText(open(mailatt, 'rb').read(), 'base64', 'gb2312')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(mailatt)
            msg.attach(att1)
        msg['to'] = mailto_list
        msg['from'] = Header('Migu-Auto<Auto@migu.com>', 'utf-8')
        msg['cc'] = mailcc
        msg['subject'] = subject

        s = smtplib.SMTP()
        s.connect(mail_host)
        s.ehlo()
        s.login(mail_user, mail_pass)
        s.sendmail(mail_user, mailto_list, msg.as_string())
        s.close()

    # 判断对象是否存在,driver表示appium连接对象，这个类中是startApp
    # UISelector.text方法;UISelector.textContains方法;UISelector.textStartsWith方法;UISelector.textMatches方法;\
    # UISelector.className方法;UISelector.classNameMatches方法;通过UiSelector.fromParent或UiObject.getFromParent方法;\
    # 通过UiSelector.childSelector或UiObject.getChild方法;UiSelector.resourceId方法;UiSelector.resourceIdMatches方法;UiSelector.description方法\
    # UiSelector.descriptionStartWith方法;UiSelector.descriptionMatches方法;参见：http://www.tuicool.com/articles/fENvUvZ
    def isExist(self, str_desc, uia_string="new UiSelector().text", driver=None, timeout=20):
        try:
            if driver is None:
                driver = self.driver
            return WebDriverWait(driver, timeout, 1). \
                until(
                lambda x: x.find_element_by_android_uiautomator(uia_string + '("' + str_desc + '")').is_displayed() \
                          or (len(x.find_elements_by_android_uiautomator(uia_string + '("' + str_desc + '")')) > 0))
        except (TimeoutException, Exception):
            # 保存错误的截图
            self.saveErrorImg(str_desc)
            return False

    # 操作对象，这里先实现click，查找元素的方法主要是find_element_by_android_uiautomator，
    # 格式为：new UiSelector().text('str_desc')
    def objClick(self, str_desc, uia_string="new UiSelector().text", driver=None):
        # 一般来说要先判断是否存在，然后再点击
        # 正常截图保存
        if driver is None:
            driver = self.driver
        self.saveRightImg(str_desc)
        driver.find_element_by_android_uiautomator(uia_string + '("' + str_desc + '")').click()

    # 根据设备分辨率从中间进行滑动，默认向下滑动
    def objSwipe(self, direction='down', driver=None):
        if driver is None:
            driver = self.driver
        size = driver.get_window_size()
        width = size['width']
        height = size['height']
        if direction == 'up':
            driver.swipe(width / 2, height / 2, width / 2, 100)
        if direction == 'down':
            driver.swipe(width / 2, height / 2, width / 2, height - 1)
        if direction == 'left':
            driver.swipe(width - 2, height / 2, 0, height / 2)
        if direction == 'right':
            driver.swipe(width / 2, height / 2, width - 1, height / 2)

    # 进行键盘输入，目前支持数字和字母
    def sendstr(self, str_code, driver=None):
        if driver is None:
            driver = self.driver
        # 定义数据字典
        key_code = {'0': '7', '1': '8', '2': '9', '3': '10', '4': '11', '5': '12', '6': '13', '7': '14', '8': '15',
                    '9': '16', 'a': '29', 'b': '30', \
                    'c': '31', 'd': '32', 'e': '33', 'f': '34', 'g': '35', 'h': '36', 'i': '37', 'j': '38', 'k': '39',
                    'l': '40', 'm': '41', 'n': '42', \
                    'o': '43', 'p': '44', 'q': '45', 'r': '46', 's': '47', 't': '48', 'u': '49', 'v': '50', 'w': '51',
                    'x': '52', 'y': '53', 'z': '54'}
        for i in range(len(str_code)):
            code = key_code[str_code[i]]
            driver.press_keycode(code)
        # 输入完毕后，输入确认
        driver.press_keycode(66)

    def print_Caseid_CaseName(self,case_id, case_name):
        u"------case_TEST001:开启录屏大师_casename------若是多个用例使用@符号分开，如：TEST001@TEST002"
        print u"------case_%s_idEnd:%s_casename------" % (case_id, case_name)
