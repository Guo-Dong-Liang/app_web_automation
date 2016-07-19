# -*- coding: UTF-8 -*-
import os
import time
import datetime
import unittest
import sys
import re
import subprocess
import codecs
from migu import HTMLTestRunner
from migu import getTestPhone
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, TimeoutException
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from Common import miguAppium
reload(sys)
sys.setdefaultencoding('utf8')

print(u'脚本被启动，开始获取参数信息')
# 获取参数,port表示appium启动的端口，resultpaht表示执行完成后报告的存储路径，udid表示执行的手机的唯一标识，可以使用adb devices命令查看
# 在初始化runuser的时候后台就会自动启动appium的服务，CurrentUser包含了所有的公共方法
CurrentUser = miguAppium.runUser(sys.argv, 'cn.emagsoftware.gamehall', '.activity.GameHallShowcase')


# 直接开始用例编写
class TestMiguGame(unittest.TestCase):
    def setUp(self):
        self.driver = CurrentUser.driver

    def test_checkUsercenter(self):
        '个人中心页面检查'
        resultstatus = True
        errorcount = 0
        print('   ')
        print('------------------start------------------')
        if CurrentUser.isExist('我的'):
            CurrentUser.objClick("我的")
        # 将账号退出登录状态
        if not CurrentUser.isExist('未登录'):
            self.driver.find_element_by_id('cn.emagsoftware.gamehall:id/menu_option').click()
            CurrentUser.objClick("用户注销")
            CurrentUser.objClick("确定")
            CurrentUser.driver.launch_app()
            if CurrentUser.isExist('我的'):
                CurrentUser.objClick("我的")
        # 查看手机是否未登录
        if CurrentUser.isExist('未登录'):
            # 点击进行登录操作
            CurrentUser.objClick('未登录')
            # 输入登录号码
            CurrentUser.sendstr('18326008529')
            # 开始密码输入
            CurrentUser.sendstr('a12345678')
            # self.driver.back()
            CurrentUser.objClick('登录')
        # 判断登录是否成功
        if CurrentUser.isExist('18326008529'):
            print(u'---【Passed】个人中心__用户登录成功__号码显示正常')
            # 个人资料检查
            CurrentUser.objClick('18326008529')
            if CurrentUser.isExist('我的资料'):
                print(u'---【Passed】个人中心__我的资料显示正常')
                self.driver.back()
                time.sleep(2)
            else:
                print(u'【Failed】个人中心__我的资料显示不正常')
                resultstatus = False
                errorcount += 1
        else:
            print(u'【Failed】个人中心__用户登录失败__用户号码显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('安徽小卡'):
            print(u'---【Passed】个人中心__用户名显示正常')
        else:
            print(u'【Failed】个人中心__用户名显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('下载中心'):
            print(u'---【Passed】个人中心__下载中心显示正常')
        else:
            print(u'【Failed】个人中心__下载中心显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('我的礼包'):
            print(u'---【Passed】个人中心__我的礼包显示正常')
        else:
            print(u'【Failed】个人中心__我的礼包显示不正常')
            resultstatus = False
            errorcount += 1
        # 这个地方现在显示的是游戏社区 20160617 eric
        if CurrentUser.isExist('游戏社区'):
            print(u'---【Passed】个人中心__游戏社区显示正常')
        else:
            print(u'【Failed】个人中心__游戏社区显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('消费记录'):
            print(u'---【Passed】个人中心__消费记录（仅页面）显示正常')
        else:
            print(u'【Failed】个人中心__消费记录显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('咪咕分享'):
            print(u'---【Passed】个人中心__咪咕分享显示正常')
        else:
            print(u'【Failed】个人中心__咪咕分享显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('充值'):
            print(u'---【Passed】个人中心__我的移动__充值按钮正常')
        else:
            print(u'【Failed】个人中心__我的移动__充值按钮不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('办理'):
            print(u'---【Passed】个人中心__我的移动__办理按钮正常')
        else:
            print(u'【Failed】个人中心__我的移动__办理按钮不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('查询'):
            print(u'---【Passed】个人中心__我的移动__查询按钮正常')
        else:
            print(u'【Failed】个人中心__我的移动__查询按钮不正常')
            resultstatus = False
            errorcount += 1
        # 判断错误信息
        if errorcount > 0:
            print('-----------------end-------------------')
            print(u'账号登录__自动登录_共计发现：{0}个错误,请查看详情：'.format(str(errorcount)))
        else:
            print('-----------------end-------------------')
        if resultstatus:
            pass
        else:
            raise Exception('出现错误')

    # 对主页面进行检查
    def test_checkHomePage(self):
        # 进行用例执行成功或者失败的标示为
        resultstatus = True
        errorcount = 0
        print('   ')
        print('------------------start------------------')
        if CurrentUser.isExist('首页'):
            print(u'---【Passed】首页__显示正常')
            CurrentUser.objClick('首页')
        else:
            print(u'【Failed】首页__显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('推荐'):
            print(u'---【Passed】首页__推荐__显示正常')
            # 开始推荐内容判断
            if CurrentUser.isExist('cn.emagsoftware.gamehall:id/top_pager', "new UiSelector().resourceId"):
                print(u'---【Passed】首页__推荐__banner显示正常')
            else:
                print(u'【Failed】首页__推荐__banner显示不正常')
                resultstatus = False
                errorcount += 1
            # 开始判断全部
            if CurrentUser.isExist('全部'):
                print(u'---【Passed】首页__推荐__全部显示正常')
                CurrentUser.objClick('全部')
                if CurrentUser.isExist('活动'):
                    CurrentUser.objClick('活动')
                    if CurrentUser.isExist('活动'):
                        print(u'---【Passed】首页__推荐__活动_点击后显示正常')
                        self.driver.back()
                    else:
                        print(u'【Failed】首页__推荐__活动_点击后显示不正常')
                        resultstatus = False
                        errorcount += 1
                else:
                    print(u'【Failed】首页__推荐__活动_显示不正常')
                    resultstatus = False
                    errorcount += 1
                # 免费礼包检查
                if CurrentUser.isExist('免费礼包'):
                    CurrentUser.objClick('免费礼包')
                    if CurrentUser.isExist('热门礼包', "new UiSelector().description"):
                        print(u'---【Passed】首页__推荐__免费礼包_点击后显示正常')
                        self.driver.back()
                    else:
                        print(u'【Failed】首页__推荐__免费礼包_点击后显示不正常')
                        self.driver.back()
                        time.sleep(2)
                        resultstatus = False
                        errorcount += 1
                else:
                    print(u'【Failed】首页__推荐__免费礼包_显示不正常')
                    resultstatus = False
                    errorcount += 1
            else:
                print(u'【Failed】首页__推荐__专题显示不正常')
                resultstatus = False
                errorcount += 1
            # 开始判断新游
            if CurrentUser.isExist('新游'):
                print(u'---【Passed】首页__推荐__新游显示正常')
                CurrentUser.objClick('新游')
                if CurrentUser.isExist('新游'):
                    print(u'---【Passed】首页__推荐__新游_点击后显示正常')
                    self.driver.back()
                else:
                    print(u'【Failed】首页__推荐__新游_点击后显示不正常')
                    resultstatus = False
                    errorcount += 1
            else:
                print(u'【Failed】首页__推荐__新游显示不正常')
                resultstatus = False
                errorcount += 1
            # 开始判断专题
            if CurrentUser.isExist('专题'):
                print(u'---【Passed】首页__推荐__专题显示正常')
                CurrentUser.objClick('专题')
                if CurrentUser.isExist('专题'):
                    print(u'---【Passed】首页__推荐__专题_点击后显示正常')
                    self.driver.back()
                else:
                    print(u'【Failed】首页__推荐__专题_点击后显示不正常')
                    resultstatus = False
                    errorcount += 1
            else:
                print(u'【Failed】首页__推荐__专题显示不正常')
                resultstatus = False
                errorcount += 1

        else:
            print(u'【Failed】首页__推荐__显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('分类'):
            print(u'---【Passed】首页__分类__显示正常')
            CurrentUser.objClick('分类')
            # 进行分类内部判断
            if CurrentUser.isExist('经典分类'):
                print(u'---【Passed】首页__分类__经典分类显示正常')
                # 点击分类中的内容
                if CurrentUser.isExist('儿童亲子'):
                    print(u'---【Passed】首页__分类__经典分类_儿童亲子显示正常')
                    CurrentUser.objClick("儿童亲子")
                    if CurrentUser.isExist('儿童亲子'):
                        print(u'---【Passed】首页__分类__经典分类_儿童亲子_点击后显示正常')
                        # 返回到分类页面
                        self.driver.back()
                    else:
                        print(u'【Failed】首页__分类__经典分类_儿童亲子_点击后显示不正常')
                        resultstatus = False
                        errorcount += 1
                else:
                    print(u'【Failed】首页__分类__经典分类_儿童亲子显示不正常')
                    resultstatus = False
                    errorcount += 1
            else:
                print(u'【Failed】首页__分类__经典分类显示不正常')
                resultstatus = False
                errorcount += 1
            # 进行滑动操作，向下
            CurrentUser.objSwipe('up')
            if CurrentUser.isExist('名门大作'):
                print(u'---【Passed】首页__分类__名门大作显示正常')
                if CurrentUser.isExist('触控科技'):
                    print(u'---【Passed】首页__分类__名门大作_触控科技显示正常')
                    CurrentUser.objClick("触控科技")
                    if CurrentUser.isExist('触控科技'):
                        print(u'---【Passed】首页__分类__名门大作_触控科技_点击后显示正常')
                        # 返回到分类页面
                        self.driver.back()
                    else:
                        print(u'【Failed】首页__分类__名门大作_触控科技_点击后显示不正常')
                        resultstatus = False
                        errorcount += 1
                else:
                    print(u'【Failed】首页__分类__名门大作_触控科技显示不正常')
                    resultstatus = False
                    errorcount += 1
            else:
                print(u'【Failed】首页__分类__名门大作显示不正常')
                resultstatus = False
                errorcount += 1
                # if CurrentUser.isExist('经典专题'):
                #     print(u'---【Passed】首页__分类__经典专题显示正常')
                #     if CurrentUser.isExist('闲来撸一把'):
                #         print(u'---【Passed】首页__分类__经典专题_闲来撸一把显示正常')
                #         CurrentUser.objClick("闲来撸一把")
                #         if CurrentUser.isExist('闲来撸一把'):
                #             print(u'---【Passed】首页__分类__经典专题_闲来撸一把_点击后显示正常')
                #             # 返回到分类页面
                #             self.driver.back()
                #         else:
                #             print(u'【Failed】首页__分类__经典专题_闲来撸一把_点击后显示不正常')
                #             resultstatus = False
                #             errorcount += 1
                #     else:
                #         print(u'【Failed】首页__分类__经典专题_闲来撸一把显示不正常')
                #         resultstatus = False
                #         errorcount += 1
                # else:
                #     print(u'【Failed】首页__分类__经典专题显示不正常')
                #     resultstatus = False
                #     errorcount += 1
        else:
            print(u'【Failed】首页__分类__显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('网游'):
            print(u'---【Passed】首页__网游__显示正常')
            # 进行网游内部展示验证
            CurrentUser.objClick('网游')
            if CurrentUser.isExist('cn.emagsoftware.gamehall:id/ivPicLogo', "new UiSelector().resourceId"):
                print(u'---【Passed】首页__网游__网游内容显示正常')
                # 网游攻略判断
                onlinegame = self.driver.find_elements_by_id('cn.emagsoftware.gamehall:id/ivPicLogo')
                dicgame = {0: '网游攻略', 1: '热门活动', 2: '礼包领取', 3: '新游推荐'}
                for i in range(len(onlinegame)):
                    onlinegame[i].click()
                    if CurrentUser.isExist(dicgame[i]):
                        print(u'---【Passed】首页__网游__{0}展示正常'.format(str(dicgame[i])))
                        self.driver.back()
                    else:
                        print(u'【Failed】首页__网游__{0}展示不正常'.format(str(dicgame[i])))
                        resultstatus = False
                        errorcount += 1
            else:
                print(u'【Failed】首页__网游__网游内容显示不正常')
                resultstatus = False
                errorcount += 1
        else:
            print(u'【Failed】首页__网游__显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('视频'):
            print(u'---【Passed】首页__视频__显示正常')
            # 查看视频内容部分
            CurrentUser.objClick('视频')
            if CurrentUser.isExist('cn.emagsoftware.gamehall:id/video_icon', "new UiSelector().resourceId"):
                print(u'---【Passed】首页__视频__视频内容显示正常')
            else:
                print(u'【Failed】首页__视频__视频内容显示不正常')
                resultstatus = False
                errorcount += 1
        else:
            print(u'【Failed】首页__视频__显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('排行'):
            print(u'---【Passed】首页__排行__显示正常')
            # 开始检查排行展示
            CurrentUser.objClick('排行')
            if CurrentUser.isExist('热评榜'):
                print(u'---【Passed】首页__排行__热评榜显示正常')
            else:
                print(u'【Failed】首页__排行__热评榜显示正常')
                resultstatus = False
                errorcount += 1
            # 进行滑动操作，使得对象可见
            CurrentUser.objSwipe('up')
            if CurrentUser.isExist('飙升榜'):
                print(u'---【Passed】首页__排行__飙升榜显示正常')
            else:
                print(u'【Failed】首页__排行__飙升榜显示不正常')
                resultstatus = False
                errorcount += 1
        else:
            print(u'【Failed】首页__排行__显示不正常')
            resultstatus = False
            errorcount += 1
        # 判断错误信息
        if errorcount > 0:
            print('-----------------end-------------------')
            print(u'首页排行页面检查_共计发现：{0}个错误,请查看详情：'.format(str(errorcount)))
        else:
            print('-----------------end-------------------')
        if resultstatus:
            pass
        else:
            raise Exception()

    def test_OnlineGame(self):
        # 进行用例执行成功或者失败的标示为
        resultstatus = True
        errorcount = 0
        print('   ')
        print('------------------start------------------')
        if CurrentUser.isExist('页游'):
            CurrentUser.objClick("页游")
        if CurrentUser.isExist('游戏', "new UiSelector().description"):
            # 对于游戏下面内容展示进行检查
            if CurrentUser.isExist('启动', "new UiSelector().description") and CurrentUser.isExist('最近玩过.*',
                                                                                                 "new UiSelector().descriptionMatches"):
                print(u'---【Passed】页游_游戏__显示正常')
        else:
            print(u'【Failed】页游_游戏__显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('排行', "new UiSelector().description"):
            print(u'---【Passed】页游_排行__显示正常')
            # 查看排行是否正常展示
            CurrentUser.objClick('排行', "new UiSelector().description")
            if CurrentUser.isExist('启动', "new UiSelector().description"):
                print(u'---【Passed】页游_游戏_排行_启动游戏显示正常')
            else:
                print(u'【Failed】页游_游戏_排行_启动游戏显示不正常')
                resultstatus = False
                errorcount += 1
        else:
            print(u'【Failed】页游_排行__显示不正常')
            resultstatus = False
            errorcount += 1
        if CurrentUser.isExist('最近玩过.*', "new UiSelector().descriptionMatches"):
            print(u'---【Passed】页游_游戏__最近玩过显示正常')
        else:
            print(u'【Failed】页游_游戏__最近玩过显示不正常')
            resultstatus = False
            errorcount += 1

        # 判断错误信息
        if errorcount > 0:
            print('-----------------end-------------------')
            print(u'页游页面检查_共计发现：{0}个错误,请查看详情：'.format(str(errorcount)))
        else:
            print('-----------------end-------------------')
        if resultstatus:
            pass
        else:
            raise Exception()

    def test_benefit(self):
        # 进行用例执行成功或者失败的标示为
        resultstatus = True
        errorcount = 0
        print('   ')
        print('------------------start------------------')
        if CurrentUser.isExist('福利'):
            print(u'---【Passed】福利_显示正常')
            CurrentUser.objClick("福利")
            if CurrentUser.isExist('活动'):
                CurrentUser.objClick('活动')
                if CurrentUser.isExist('活动'):
                    print(u'---【Passed】福利__活动_点击后显示正常')
                    if CurrentUser.isExist('网游活动'):
                        print(u'---【Passed】福利__活动_网游活动显示正常')
                    else:
                        print(u'【Failed】福利__活动_网游活动显示不正常')
                        resultstatus = False
                        errorcount += 1
                    if CurrentUser.isExist('单机活动'):
                        print(u'---【Passed】福利__活动_单机活动显示正常')
                    else:
                        print(u'【Failed】福利__活动_单机活动显示不正常')
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                else:
                    print(u'【Failed】福利__活动_点击后显示不正常')
                    self.driver.back()
                    resultstatus = False
                    errorcount += 1
            else:
                print(u'【Failed】福利__活动_显示不正常')
                self.driver.back()
                resultstatus = False
                errorcount += 1
            # 免费礼包检查
            if CurrentUser.isExist('免费礼包'):
                CurrentUser.objClick('免费礼包')
                if CurrentUser.isExist('热门礼包', "new UiSelector().description"):
                    print(u'---【Passed】福利__免费礼包_热门礼包显示正常')
                else:
                    print(u'【Failed】福利__免费礼包_热门礼包显示不正常')
                    resultstatus = False
                    errorcount += 1
                # 会员礼包变更为热门礼包  eric 20160623
                if CurrentUser.isExist('热门礼包', "new UiSelector().description"):
                    print(u'---【Passed】福利__热门礼包_会员礼包显示正常')
                else:
                    print(u'【Failed】福利__热门礼包_会员礼包显示不正常')
                    resultstatus = False
                    errorcount += 1

                if CurrentUser.isExist('最新礼包', "new UiSelector().description"):
                    print(u'---【Passed】福利__免费礼包_最新礼包显示正常')
                else:
                    print(u'【Failed】福利__免费礼包_最新礼包显示不正常')
                    resultstatus = False
                    errorcount += 1

                self.driver.back()
            else:
                print(u'【Failed】福利__免费礼包_显示不正常')
                resultstatus = False
                errorcount += 1
            # 检查会员中心
            if CurrentUser.isExist('会员中心'):
                CurrentUser.objClick('会员中心')
                if CurrentUser.isExist('普通用户', "new UiSelector().description"):
                    print(u'---【Passed】福利__会员中心_普通用户显示正常')
                else:
                    print(u'【Failed】福利__会员中心_普通用户显示不正常')
                    resultstatus = False
                    errorcount += 1
                if CurrentUser.isExist('白银会员', "new UiSelector().description"):
                    print(u'---【Passed】福利__会员中心_白银会员显示正常')
                else:
                    print(u'【Failed】福利__会员中心_白银会员显示不正常')
                    resultstatus = False
                    errorcount += 1
                if CurrentUser.isExist('黄金会员', "new UiSelector().description"):
                    print(u'---【Passed】福利__会员中心_黄金会员显示正常')
                else:
                    print(u'【Failed】福利__会员中心_黄金会员显示不正常')
                    resultstatus = False
                    errorcount += 1
                self.driver.back()
            else:
                print(u'【Failed】福利__会员中心_显示不正常')
                self.driver.back()
                resultstatus = False
                errorcount += 1
        else:
            print(u'【Failed】福利_显示不正常')
            resultstatus = False
            errorcount += 1

        # 判断错误信息
        if errorcount > 0:
            print('-----------------end-------------------')
            print(u'福利页面检查_共计发现：{0}个错误,请查看详情：'.format(str(errorcount)))
        else:
            print('-----------------end-------------------')
        if resultstatus:
            pass
        else:
            raise Exception()

    # 左边侧功能栏检查
    def test_leftfunction(self):
        # 进行用例执行成功或者失败的标示为
        resultstatus = True
        errorcount = 0
        print('   ')
        print('------------------start------------------')
        # 进行滑动操作，展示左边功能栏
        # self.driver.swipe(60, 800, 360, 800)
        if CurrentUser.isExist('cn.emagsoftware.gamehall:id/to_left', "new UiSelector().resourceId"):
            print(u'---【Passed】左边功能栏按钮显示正常')
            CurrentUser.objClick('cn.emagsoftware.gamehall:id/to_left', "new UiSelector().resourceId")
            # 开始检查左边功能栏显示,财务管理被去除--20160523
            checklist = ['安徽小卡', '18326008529', '等级:', '战斗值:', '首页', '小编推荐', '网游攻略', '在线客服', \
                         '帮助中心', '站内信', '充值', '热门活动', '会员', '检查更新', '咪咕善跑', '手柄设置', '设置', '注销']
            for check in checklist:
                if CurrentUser.isExist(check):
                    print(u'---【Passed】左边功能栏__{0}显示正常'.format(str(check)))
                else:
                    print(u'【Failed】左边功能栏__{0}显示不正常'.format(str(check)))
                    resultstatus = False
                    errorcount += 1
            # 对转跳功能检查
            # 个人头像
            if CurrentUser.isExist('cn.emagsoftware.gamehall:id/header', "new UiSelector().resourceId"):
                print(u'---【Passed】左边功能栏__个人头像按钮显示正常')
                CurrentUser.objClick('cn.emagsoftware.gamehall:id/header', "new UiSelector().resourceId")
                if CurrentUser.isExist('下载中心'):
                    print(u'---【Passed】左边功能栏__个人头像按钮__转跳显示正常（出现下载中心）')
                else:
                    print(u'【Failed】左边功能栏__个人头像按钮__转跳显示不正常（没有现下载中心）')
                self.driver.back()
            else:
                print(u'【Failed】左边功能栏__个人头像按钮显示不正常')
            self.driver.back()
            # 对于其他转跳的验证，20160523 财务管理被去除
            checklist_child = ['首页', '小编推荐', '网游攻略', '在线客服', '帮助中心', '站内信',
                               '充值', '热门活动', '会员', '检查更新', '咪咕善跑', '手柄设置', '设置', '注销']
            for redictcheck in checklist_child:
                # 点击链接
                CurrentUser.objClick(redictcheck)
                # 开始校验
                if redictcheck == '首页':
                    if CurrentUser.isExist('我的'):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                        CurrentUser.objClick('cn.emagsoftware.gamehall:id/to_left', "new UiSelector().resourceId")
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                        CurrentUser.objClick('cn.emagsoftware.gamehall:id/to_left', "new UiSelector().resourceId")
                elif redictcheck == '小编推荐':
                    if CurrentUser.isExist('cn.emagsoftware.gamehall:id/tvInformationTitle',
                                           'new UiSelector().resourceId') and CurrentUser.isExist(
                        'cn.emagsoftware.gamehall:id/tvInformationSummary',
                        "new UiSelector().resourceId") and CurrentUser.isExist(redictcheck):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '网游攻略':
                    if CurrentUser.isExist('cn.emagsoftware.gamehall:id/tvInformationTitle',
                                           'new UiSelector().resourceId') and CurrentUser.isExist(
                        'cn.emagsoftware.gamehall:id/tvInformationSummary',
                        "new UiSelector().resourceId") and CurrentUser.isExist(redictcheck):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '在线客服':
                    if CurrentUser.isExist('IM客服', 'new UiSelector().description') and CurrentUser.isExist(
                            '请点击选择您需要帮助的业务类型:',
                            "new UiSelector().description") and CurrentUser.isExist(
                        'send', "new UiSelector().description"):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '帮助中心':
                    if CurrentUser.isExist('问题与帮助中心', 'new UiSelector().description') and CurrentUser.isExist('业务介绍 >',
                                                                                                              "new UiSelector().description") and CurrentUser.isExist(
                        '操作使用 >', "new UiSelector().description"):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '站内信':
                    if CurrentUser.isExist('cn.emagsoftware.gamehall:id/tvNotificationContent',
                                           'new UiSelector().resourceId') and CurrentUser.isExist(
                        'cn.emagsoftware.gamehall:id/tvNotificationName',
                        "new UiSelector().resourceId") and CurrentUser.isExist(redictcheck):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '充值':
                    if CurrentUser.isExist('点数充值') and CurrentUser.isExist('交易信息') and CurrentUser.isExist(
                            '请选择充值方式:') and CurrentUser.isExist(
                            redictcheck):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '财务管理':
                    if CurrentUser.isExist('查流量') and CurrentUser.isExist('查话费') and CurrentUser.isExist('本月资费') \
                            and CurrentUser.isExist(redictcheck):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '热门活动':
                    if CurrentUser.isExist('网游活动') and CurrentUser.isExist('单机活动') and CurrentUser.isExist(redictcheck):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '会员':
                    if CurrentUser.isExist('普通用户', "new UiSelector().description") and \
                            CurrentUser.isExist('白银会员', "new UiSelector().description") and CurrentUser.isExist(
                        redictcheck):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '检查更新':
                    pass
                elif redictcheck == '咪咕善跑':
                    if CurrentUser.isExist('号码归属地') and CurrentUser.isExist('线上排名') and CurrentUser.isExist(
                            redictcheck):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '手柄设置':
                    if CurrentUser.isExist('手柄型号') and CurrentUser.isExist('手柄电量') and CurrentUser.isExist('固件版本') \
                            and CurrentUser.isExist('连接状态') and CurrentUser.isExist(redictcheck):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '设置':
                    if CurrentUser.isExist('下载安装设置') and CurrentUser.isExist('网络设置') and CurrentUser.isExist('消息设置') \
                            and CurrentUser.isExist(redictcheck):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
                elif redictcheck == '注销':
                    if CurrentUser.isExist('确定要注销么') and CurrentUser.isExist('取消') and CurrentUser.isExist('确定'):
                        print(u'---【Passed】左边功能栏__{0}__转跳显示正常'.format(str(redictcheck)))
                    else:
                        print(u'【Failed】左边功能栏__{0}__转跳显示不正常'.format(str(redictcheck)))
                        resultstatus = False
                        errorcount += 1
                    self.driver.back()
            self.driver.back()
        else:
            print(u'【Failed】左边功能栏按钮显示不正常')
            resultstatus = False
            errorcount += 1
        # 判断错误信息
        if errorcount > 0:
            print('-----------------end-------------------')
            print(u'左边功能栏页面检查_共计发现：{0}个错误,请查看详情：'.format(str(errorcount)))
        else:
            print('-----------------end-------------------')
        if resultstatus:
            pass
        else:
            raise Exception()

    # 右边侧功能栏检查
    def test_rightfunction(self):
        '右边功能页面检查'
        # 进行用例执行成功或者失败的标示为
        resultstatus = True
        errorcount = 0
        print('   ')
        print('------------------start------------------')
        # 进行滑动操作，展示左边功能栏
        # self.driver.swipe(60, 800, 360, 800)
        if CurrentUser.isExist('cn.emagsoftware.gamehall:id/to_right', "new UiSelector().resourceId"):
            print(u'---【Passed】右边功能栏按钮显示正常')
            CurrentUser.objClick('cn.emagsoftware.gamehall:id/to_right', "new UiSelector().resourceId")
            # 开始检查右边功能栏显示
            checklist = ['扫一扫', '一键加速']
            for check in checklist:
                if CurrentUser.isExist(check):
                    print(u'---【Passed】右边功能栏__{0}显示正常'.format(str(check)))
                else:
                    print(u'【Failed】右边功能栏__{0}显示不正常'.format(str(check)))
                    resultstatus = False
                    errorcount += 1
            self.driver.back()
        else:
            print(u'【Failed】右边功能栏按钮显示不正常')
            resultstatus = False
            errorcount += 1
        # 判断错误信息
        if errorcount > 0:
            print('-----------------end-------------------')
            print(u'左边功能栏页面检查_共计发现：{0}个错误,请查看详情：'.format(str(errorcount)))
        else:
            print('-----------------end-------------------')
        if resultstatus:
            pass
        else:
            raise Exception()

    # 搜索、下载功能检查
    def test_searchdownload(self):
        # 进行用例执行成功或者失败的标示为
        resultstatus = True
        errorcount = 0
        print('   ')
        print('------------------start------------------')
        # 进行滑动操作，展示左边功能栏
        # self.driver.swipe(60, 800, 360, 800)
        # 搜索功能
        if CurrentUser.isExist('cn.emagsoftware.gamehall:id/btn_index_search', "new UiSelector().resourceId"):
            print(u'---【Passed】搜索按钮显示正常')
            # 查看搜索功能
            CurrentUser.objClick('cn.emagsoftware.gamehall:id/btn_index_search', "new UiSelector().resourceId")
            if CurrentUser.isExist('cn.emagsoftware.gamehall:id/btnSearchDel', "new UiSelector().resourceId"):
                print(u'---【Passed】搜索按钮__清除文本按钮__显示正常')
                # 删除搜索文本
                CurrentUser.objClick('cn.emagsoftware.gamehall:id/btnSearchDel', "new UiSelector().resourceId")
                CurrentUser.objClick('cn.emagsoftware.gamehall:id/actvSearch', "new UiSelector().resourceId")
                CurrentUser.sendstr('ddz')
                # 输入smtw
                # self.driver.press_keycode(66)
                time.sleep(2)
                CurrentUser.objClick('cn.emagsoftware.gamehall:id/btnSearchKeywords', "new UiSelector().resourceId")
                if CurrentUser.isExist('斗地主单机'):
                    print(u'---【Passed】搜索按钮__搜索结果__显示正常')
                else:
                    print(u'【Failed】搜索按钮__搜索结果__显示不正常')
                    resultstatus = False
                    errorcount += 1
            else:
                print(u'【Failed】搜索按钮__点击进入后显示不正常')
                resultstatus = False
                errorcount += 1
            self.driver.back()
        else:
            print(u'【Failed】搜索按钮显示不正常')
            resultstatus = False
            errorcount += 1
        # 下载功能
        if CurrentUser.isExist('cn.emagsoftware.gamehall:id/download', "new UiSelector().resourceId"):
            print(u'---【Passed】下载按钮显示正常')
            # 查看下载功能
            CurrentUser.objClick('cn.emagsoftware.gamehall:id/download', "new UiSelector().resourceId")
            checklist = ['下载管理', '下载中心', '可更新']
            for check in checklist:
                if CurrentUser.isExist(check):
                    print(u'---【Passed】下载功能__{0}显示正常'.format(str(check)))
                else:
                    print(u'【Failed】下载功能__{0}显示不正常'.format(str(check)))
                    resultstatus = False
                    errorcount += 1
            self.driver.back()
        else:
            print(u'【Failed】搜索按钮显示不正常')
            resultstatus = False
            errorcount += 1

        # 判断错误信息
        if errorcount > 0:
            print('-----------------end-------------------')
            print(u'搜索下载功能栏页面检查_共计发现：{0}个错误,请查看详情：'.format(str(errorcount)))
        else:
            print('-----------------end-------------------')
        if resultstatus:
            pass
        else:
            raise Exception()

    def tearDown(self):
        self.driver = CurrentUser.driver


if __name__ == '__main__':
    try:
        testsuite = unittest.TestSuite()
        # for test in dir(TestMiguGame):
        #     if test.startswith('test_'):
        #         testsuite.addTest(TestMiguGame(test))
        testsuite.addTest(TestMiguGame("test_checkUsercenter"))
        # testsuite.addTest(TestMiguGame("test_checkHomePage"))
        # testsuite.addTest(TestMiguGame("test_OnlineGame"))
        # testsuite.addTest(TestMiguGame("test_benefit"))
        # testsuite.addTest(TestMiguGame("test_leftfunction"))
        # testsuite.addTest(TestMiguGame("test_rightfunction"))
        # testsuite.addTest(TestMiguGame("test_searchdownload"))
        print CurrentUser.resultpath
        fp = file(CurrentUser.resultpath, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=u'咪咕游戏测试报告',
            description=u'咪咕游戏,本次检查设定默认等待时间为：20秒，超过20秒没有展示就认为存在错误'
        )
        runner.run(testsuite)
        fp.close()

        # 更新数据库执行状态可执行
        CurrentUser.updatebysql('', status='canrun')
        # 发送邮件通知
        CurrentUser.sendemail(u'咪咕游戏-自动化测试报告', \
                              u'你好<br />咪咕游戏功能检查任务已经执行完成，详细记录已经在附件报告中，请您仔细查阅。<br />' + \
                              u'<br /><br /><br /><br /><br />B.R.<br />咪咕技术组<br />联系方式：dongliang.guo@h3c.com'
                              , CurrentUser.useremail, 'dongliang.guo@h3c.com',
                              CurrentUser.resultpath)
    except Exception, e:
        print(u'stop python')
        CurrentUser.updatebysql('', status='runfail')
        CurrentUser.sendemail(u'启动咪咕游戏报错', u'你好<br />请查看服务器是否运行正常<br />错误信息:<br />' + str(e)+\
                              u'<br /><br /><br /><br /><br />B.R.<br />咪咕技术组<br />联系方式：dongliang.guo@h3c.com', CurrentUser.useremail,
                              'dongliang.guo@h3c.com')
        # 更新数据库状态，执行失败
        sys.exit(0)
