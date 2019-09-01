#!/usr/bin/env python
# -*- coding:utf-8 –*-
import wx
import time
# import helpers
from threading import Thread
import random
import roslibpy
import re
import json
import logging

class Page:
    Map_line_point, Map_line_size, Map_line_direction = range(3)
    list_line_map_info = [
        [wx.Point(17, 20), wx.Size(420, 2), wx.LI_HORIZONTAL],
        [wx.Point(17, 20), wx.Size(2, 640 + 100), wx.LI_VERTICAL],
        [wx.Point(17+420, 20), wx.Size(2, 640 + 100), wx.LI_VERTICAL],
        [wx.Point(17, 20 + 640 + 100), wx.Size(420, 2), wx.LI_HORIZONTAL],
        [wx.Point(17 + 50, 40), wx.Size(370, 2), wx.LI_HORIZONTAL],
        [wx.Point(17 + 50, 40+60), wx.Size(370, 2), wx.LI_HORIZONTAL],
        [wx.Point(17 + 50, 40 + 340 + 50), wx.Size(370, 2), wx.LI_HORIZONTAL],
        [wx.Point(17 + 420 + 30, 20), wx.Size(700, 2), wx.LI_HORIZONTAL],
        [wx.Point(17 + 420 + 30, 20), wx.Size(2, 640 + 100), wx.LI_VERTICAL],
        [wx.Point(17 + 420 + 30 + 700, 20), wx.Size(2, 640 + 100), wx.LI_VERTICAL],
        [wx.Point(17 + 420 + 30, 20 + 640 + 100), wx.Size(700, 2), wx.LI_HORIZONTAL],
        [wx.Point(520, 40), wx.Size(650, 2), wx.LI_HORIZONTAL],
        [wx.Point(520, 40 + 370), wx.Size(650, 2), wx.LI_HORIZONTAL],
        # [wx.Point(40, 500), wx.Size(400, 2), wx.LI_HORIZONTAL]
    ]

    label_line_point, label_line_size, label_line_string = range(3)
    list_label_info = [
        [wx.Point(17 + 10, 30), wx.Size(40, 20), '连接'],
        [wx.Point(17 + 10, 30 + 60), wx.Size(40, 20), 'node'],
        [wx.Point(17 + 10, 30 + 340 + 50), wx.Size(40, 20), 'service'],
        [wx.Point(480, 30), wx.Size(40, 20), 'param'],
        [wx.Point(480, 400), wx.Size(40, 20), 'topic'],
        [wx.Point(720, 475), wx.Size(60, 20), '间隔/ms'],
        [wx.Point(677, 510), wx.Size(60, 20), 'name:'],
        [wx.Point(677, 540), wx.Size(60, 20), 'type:'],
        [wx.Point(677, 570), wx.Size(100, 20), 'message detail'],
        # [wx.Point(40, 500), wx.Size(400, 2), wx.LI_HORIZONTAL]
    ]


class TaskThread(Thread):
    """这是一个主任务线程"""

    def __init__(self, frame):
        Thread.__init__(self)
        self.frame = frame

    def run(self):
        showcnt = 0
        sendcnt = 0
        while self.frame.taskrun:
            time.sleep(0.05)
            if self.frame.client.is_connected:
                sendcnt += 1
                if sendcnt >= 20:
                    # self.frame.talk_topic.publish(roslibpy.Message({"battery": 100, "run_status": True, "speed": 0.7,
                    #                                                 "water": 80}))
                    sendcnt = 0
                pass

            if self.frame.connect_staus == '连接中':
                # print(self.frame.hostname)
                try:
                    # print(self.frame.client.)
                    self.frame.client.run(timeout = 2)
                except Exception as err:
                    # self.client.terminate()
                    print(err)

                if self.frame.client.is_connected:
                    self.frame.connect_staus = '连接成功'
                    self.frame.m_buttonconnect.SetLabelText('连接成功')
                else:
                    self.frame.connect_staus = '连接失败'
                    self.frame.m_buttonconnect.SetLabelText('连接失败')
            elif self.frame.connect_staus == '断开中':
                self.frame.client.close()
                self.frame.connect_staus = '已断开'

            elif self.frame.connect_staus == '连接成功':
                showcnt += 1
                if showcnt >= 20:
                    self.frame.m_buttonconnect.SetLabelText('断开')
                    self.frame.connect_staus = '已连接'
                    showcnt = 0
            elif self.frame.connect_staus == '连接失败':
                showcnt += 1
                if showcnt >= 20:
                    self.frame.m_buttonconnect.SetLabelText('连接')
                    self.frame.connect_staus = '未连接'
                    showcnt = 0
            elif self.frame.connect_staus == '已断开':
                showcnt += 1
                if showcnt >= 20:
                    self.frame.m_buttonconnect.SetLabelText('连接')
                    self.frame.connect_staus = '未连接'
                    showcnt = 0
        pass
        self.frame.client.terminate()

class MyFrame(wx.Frame):
    """这个是整个显示的类"""

    def __init__(self, parent):
        """初始化整个空间和一些参数"""
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='rosbridge 测试', pos=wx.Point(0, 0), size=wx.Size(1200, 820))
        self.panel = wx.Panel(self, -1)
        self.Center()  # 设置弹窗在屏幕中间
        self.SetFocus()  # 不要焦点
        self.hostname = '192.168.0.125'
        self.hostport = '9090'
        self.taskrun = True
        self.connect_staus = '未连接'

        self.client = roslibpy.Ros(host=self.hostname, port=int(self.hostport))

        # self.talk_topic = roslibpy.Topic(self.client, '/chatter/self', 'beginner_tutorials/testjin')
        # self.listener = roslibpy.Topic(self.client, '/chatter', 'std_msgs/String')
        # self.client.on_ready(self.start_receiving,run_in_thread=True)

        self.m_textCtrlip = wx.TextCtrl(self.panel, wx.ID_ANY, self.hostname , wx.Point(37, 60), wx.Size(100, 20),
                                        0 | wx.TE_CENTER)
        self.m_textCtrlport = wx.TextCtrl(self.panel, wx.ID_ANY, str(self.hostport), wx.Point(174, 60),
                                          wx.Size(50, 20), 0 | wx.TE_CENTER)

        self.m_buttonconnect = wx.Button(self.panel, wx.ID_ANY, '连接', wx.Point(239, 60), wx.Size(80, 20), 0)
        self.m_buttonclear = wx.Button(self.panel, wx.ID_ANY, '清空', wx.Point(334, 60), wx.Size(80, 20), 0)

        # node list and detail
        self.m_buttongetnode = wx.Button(self.panel, wx.ID_ANY, 'Node list', wx.Point(37, 120), wx.Size(100, 20), 0)
        self.m_buttonclearnode = wx.Button(self.panel, wx.ID_ANY, 'clear', wx.Point(174, 120), wx.Size(100, 20), 0)
        self.m_listBoxnodedetail= []
        self.m_listBoxnode = wx.ListBox( self.panel, wx.ID_ANY, wx.Point(37, 160), wx.Size(100, 250),
                                         self.m_listBoxnodedetail, 0 | wx.HSCROLL)
        self.m_textnode = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(174, 160), wx.Size(240, 250),
                                    style=wx.TE_MULTILINE)

        # service list and detail
        self.m_buttongetservice = wx.Button(self.panel, wx.ID_ANY, 'service list', wx.Point(37, 450), wx.Size(100, 20),
                                            0)
        self.m_buttonclearservice = wx.Button(self.panel, wx.ID_ANY, 'clear', wx.Point(274, 450), wx.Size(100, 20), 0)
        self.m_listBoxservicedetail = []
        self.m_listBoxservice = wx.ListBox(self.panel, wx.ID_ANY, wx.Point(37, 490), wx.Size(200, 250),
                                        self.m_listBoxservicedetail, 0 | wx.HSCROLL)
        self.m_textservice = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(274, 490), wx.Size(140, 250),
                                      style=wx.TE_MULTILINE)

        # param list and detail
        self.m_buttongetparam = wx.Button(self.panel, wx.ID_ANY, 'param list', wx.Point(487, 60), wx.Size(75, 25),  0)
        self.m_buttonclearparam = wx.Button(self.panel, wx.ID_ANY, 'clear', wx.Point(582, 60), wx.Size(75, 25), 0)
        self.m_buttonparamget = wx.Button(self.panel, wx.ID_ANY, 'get', wx.Point(677, 60), wx.Size(75, 25), 0)
        self.m_buttonparamset = wx.Button(self.panel, wx.ID_ANY, 'set', wx.Point(789, 60), wx.Size(75, 25), 0)

        self.m_listBoxparamdetail = []
        self.m_listBoxparam = wx.ListBox(self.panel, wx.ID_ANY, wx.Point(487, 140), wx.Size(265, 250),
                                         self.m_listBoxparamdetail, 0 | wx.HSCROLL)
        self.m_textparam = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(789, 100), wx.Size(355, 290),
                                       style=wx.TE_MULTILINE)
        self.m_textparamset = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(884, 60), wx.Size(260, 25))
        self.m_textparamfilter = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(487, 100), wx.Size(265, 25)
                                             )

        # topic list and detail
        self.m_buttongettopic = wx.Button(self.panel, wx.ID_ANY, 'topic list', wx.Point(487, 430), wx.Size(60, 25), 0)
        self.m_buttoncleartopic = wx.Button(self.panel, wx.ID_ANY, 'clear', wx.Point(577, 430), wx.Size(60, 25), 0)
        self.m_buttontopicsub = wx.Button(self.panel, wx.ID_ANY, 'subscribe', wx.Point(887, 430), wx.Size(120, 25), 0)
        self.m_buttontopicunsub = wx.Button(self.panel, wx.ID_ANY, 'unsubscribe', wx.Point(1027, 430), wx.Size(120, 25), 0
                                            )
        self.m_buttontopicpub = wx.Button(self.panel, wx.ID_ANY, 'publish', wx.Point(677, 430), wx.Size(170, 25),
                                            0)
        self.m_checkBox_auto = wx.CheckBox(self.panel, wx.ID_ANY, '自动', wx.Point(677, 470), wx.Size(50, 25), 0)

        self.m_listBoxtopicdetail = []
        self.m_listBoxtopicdetailshow = []
        self.m_listBoxtopic = wx.ListBox(self.panel, wx.ID_ANY, wx.Point(487, 510), wx.Size(150, 230),
                                         self.m_listBoxparamdetail, 0 | wx.HSCROLL)

        self.m_texttopic = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(697 + 190, 470),
                                       wx.Size(260, 270),
                                       style=wx.TE_MULTILINE)
        self.m_texttopicsettime = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(787, 470),
                                          wx.Size(60, 25))
        self.m_texttopicsettime.SetValue('1000')
        self.m_texttopicfilter = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(487, 470),
                                             wx.Size(150, 25))

        self.m_texttopicpubname = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(747, 510),
                                              wx.Size(100, 25))
        self.m_texttopicpubname.SetValue('/hello_world')

        self.m_texttopicpubmessagetype = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(747, 540),
                                              wx.Size(100, 25))
        self.m_texttopicpubmessagetype.SetValue('std_msgs/String')

        self.m_texttopicpubmessage = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.Point(677, 600),
                                                     wx.Size(170, 140))
        self.m_texttopicpubmessage.SetValue('{\'data\':\'hello world\'}')

        self.topic_pub = None

        self.task = TaskThread(self)
        self.task.start()
        self.Bind(wx.EVT_CLOSE,self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.On_Click_connct, self.m_buttonconnect)
        self.Bind(wx.EVT_BUTTON, self.OnClickClear, self.m_buttonclear)
        self.m_textCtrlip.Bind(wx.EVT_TEXT,self.OnTextChange)
        self.m_textCtrlport.Bind(wx.EVT_TEXT, self.OnTextChange)
        self.m_textparamfilter.Bind(wx.EVT_TEXT, self.OnFilterTextChange)
        self.m_texttopicfilter.Bind(wx.EVT_TEXT, self.OnFilterTextChangeTopic)

        self.Bind(wx.EVT_BUTTON, self.OnClickgetnode, self.m_buttongetnode)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxSelect,self.m_listBoxnode)
        self.Bind(wx.EVT_BUTTON, self.OnClearnode, self.m_buttonclearnode)

        self.Bind(wx.EVT_BUTTON, self.OnClickgetservice, self.m_buttongetservice)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxSelectservice, self.m_listBoxservice)
        self.Bind(wx.EVT_BUTTON, self.OnClearservice, self.m_buttonclearservice)

        self.Bind(wx.EVT_BUTTON, self.OnClickgetparam, self.m_buttongetparam)
        self.Bind(wx.EVT_BUTTON, self.OnClickparamset, self.m_buttonparamset)
        self.Bind(wx.EVT_BUTTON, self.OnClickparamget, self.m_buttonparamget)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxSelectparam, self.m_listBoxparam)
        self.Bind(wx.EVT_BUTTON, self.OnClearparam, self.m_buttonclearparam)

        self.topicsubdict = {}
        self.Bind(wx.EVT_BUTTON, self.OnClickgettopic, self.m_buttongettopic)
        self.Bind(wx.EVT_BUTTON, self.OnClicktopicsub, self.m_buttontopicsub)
        self.Bind(wx.EVT_BUTTON, self.OnClicktopicunsub, self.m_buttontopicunsub)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxSelecttopic, self.m_listBoxtopic)
        self.Bind(wx.EVT_BUTTON, self.OnCleartopic, self.m_buttoncleartopic)
        self.m_buttontopicpub.Bind(wx.EVT_BUTTON, self.OnClicktopicpub)
        self.m_checkBox_auto.Bind(wx.EVT_CHECKBOX, self.OnClickautosend)

        # 修饰线条
        for index in range(len(Page.list_line_map_info)):
            static_line = wx.StaticLine(self.panel, wx.ID_ANY, Page.list_line_map_info[index][Page.Map_line_point],
                                        Page.list_line_map_info[index][Page.Map_line_size],
                                        Page.list_line_map_info[index][Page.Map_line_direction])

        for index in range(len(Page.list_label_info)):
            static_line = wx.StaticText(self.panel, wx.ID_ANY, Page.list_label_info[index][Page.label_line_string],
                                        Page.list_label_info[index][Page.label_line_point],
                                        Page.list_label_info[index][Page.label_line_size],
                                        0 | wx.ALIGN_RIGHT)

        self.selecttopic = None
        self.selectparam = None

        self.timer_publish = wx.Timer(self)  # 创建定时器
        self.Bind(wx.EVT_TIMER, self.on_timer_publish, self.timer_publish)  # 绑定一个定时器事件

    def on_timer_publish(self, event):
        self.OnClicktopicpub(event)

        # 这是topic的地方
    def OnFilterTextChangeTopic(self, event):
        if str(self.m_texttopicfilter.GetValue()) == '':
            self.m_listBoxtopic.Clear()
            self.m_listBoxtopic.AppendItems(self.m_listBoxtopicdetail)
        else:
            str_value = str(self.m_texttopicfilter.GetValue())
            list_show = []
            # print('type',type(self))
            for list in self.m_listBoxtopicdetail:
                # print(list)
                if str_value in list:
                    list_show.append(list)
            self.m_listBoxtopic.Clear()
            self.m_listBoxtopic.AppendItems(list_show)
        pass

    def OnCleartopic(self, event):
        self.m_texttopic.Clear()
        # self.m_texttopicsettime.Clear()

    def topictypecallback(self,data):
        self.topictype = data['type']
        print(self.topictype)
        if self.topicselectname in self.topicsubdict:
            self.selecttopic = self.topicsubdict[self.topicselectname]
            pass
        else:
            self.selecttopic = roslibpy.Topic(self.client, self.topicselectname, self.topictype)
            self.topicsubdict[self.topicselectname] =self.selecttopic

    def OnListBoxSelecttopic(self, event):
        index = self.m_listBoxtopic.GetSelection()
        self.topicselectname = self.m_listBoxtopic.GetItems()[index]
        self.client.get_topic_type(self.topicselectname,self.topictypecallback)

        str_line = '-----------------------\n'
        self.m_texttopic.AppendText(str_line + self.topicselectname + '\n' + str_line)

    def gettopicdetailcallback(self, data):
        # print(data)
        self.m_texttopic.AppendText('\ngettopic\n' + self.topicselectname + '\nresult:\n')
        str_line = '-----------------------\n'
        self.m_texttopic.AppendText(str_line)
        self.m_texttopic.AppendText(str(data) + '\n')
        self.m_texttopic.AppendText(str_line)
        # jsontest = json.dumps(dict(data), sort_keys=True, indent=2, separators=(',', ': '))
        # self.m_textparam.AppendText(jsontest)
        # print(jsontest)

    def subtopicdetailcallback(self, data):
        # print(data)
        jsontest = json.dumps(dict(data), sort_keys=True, indent=2, separators=(',', ': '))
        strtime = str(int(time.time_ns()/1000000))
        self.m_texttopic.AppendText('\ntopic echo \n' + self.topicselectname + '\nresult: --' + strtime + '\n')
        str_line = '-----------------------\n'
        self.m_texttopic.AppendText(str_line)
        self.m_texttopic.AppendText(str(jsontest) + '\n')
        self.m_texttopic.AppendText(str_line)

    def OnClicktopicsub(self, event):
        if self.selecttopic:
            if self.selecttopic.is_subscribed:
                pass
            else:
                self.selecttopic.subscribe(self.subtopicdetailcallback)
            pass

    def OnClicktopicunsub(self, event):
        if self.selecttopic:
            self.selecttopic.unsubscribe()
        pass

    def OnClickautosend(self, event):
        if self.client.is_connected:
            if self.m_checkBox_auto.GetValue():
                self.timer_publish.Stop()
                self.timer_publish.Start(int(self.m_texttopicsettime.GetValue()))
            else:
                self.timer_publish.Stop()
        pass

    def OnClicktopicpub(self, event):
        if self.client.is_connected:
            strpubname = str(self.m_texttopicpubname.GetValue())
            strpubmessagetype = str(self.m_texttopicpubmessagetype.GetValue())
            strpubmessage = str(self.m_texttopicpubmessage.GetValue())
            dictpub = ''
            try:
                dictpub = eval(strpubmessage)
            except Exception as e:
                if self.timer_publish.IsRunning():
                    self.timer_publish.Stop()
                    self.m_checkBox_auto.SetValue(False)
                dlg = wx.MessageDialog(None, '消息格式错误，请检查是否为json格式', '消息格式错误', wx.OK)
                if dlg.ShowModal() == wx.ID_OK:
                    pass
                else:
                    pass
                dlg.Destroy()
            if strpubname is not '':
                if strpubmessagetype is not '':
                    if self.topic_pub is None:
                        self.topic_pub = roslibpy.Topic(self.client,strpubname,strpubmessagetype)
                        self.topic_pub.publish(roslibpy.Message(dictpub))
                    else:
                        if self.topic_pub.name is not strpubname:
                            if self.topic_pub.is_advertised:
                                self.topic_pub.unadvertise()

                        self.topic_pub = roslibpy.Topic(self.client,strpubname,strpubmessagetype)
                        self.topic_pub.publish(roslibpy.Message(dictpub))


    def OnClickgettopic(self, event):
        if self.client.is_connected:
            # print('haha')
            self.client.get_topics(self.topiccallback)

    def topiccallback(self, data):
        self.m_listBoxtopicdetail = data['topics']
        self.m_listBoxtopic.Clear()
        self.m_listBoxtopic.AppendItems(self.m_listBoxtopicdetail)

        # 这是param的地方
    def OnFilterTextChange(self, event):
        if str(self.m_textparamfilter.GetValue()) == '':
            self.m_listBoxparam.Clear()
            self.m_listBoxparam.AppendItems(self.m_listBoxparamdetail)
        else:
            str_value = str(self.m_textparamfilter.GetValue())
            list_show = []
            # print('type',type(self))
            for list in self.m_listBoxparamdetail:
                # print(list)
                if str_value in list:
                    list_show.append(list)
            self.m_listBoxparam.Clear()
            self.m_listBoxparam.AppendItems(list_show)
        pass

    def OnClearparam(self, event):
        self.m_textparam.Clear()
        self.m_textparamset.Clear()

    def OnListBoxSelectparam(self, event):
        index = self.m_listBoxparam.GetSelection()
        self.paramselectname = self.m_listBoxparam.GetItems()[index]
        self.selectparam = roslibpy.Param(self.client, self.paramselectname)
        # self.selectparam.get(self.getparamdetailcallback)
        # str_show = 'getparam  \n'+ self.paramselectname
        str_line = '-----------------------\n'
        self.m_textparam.AppendText( str_line + self.paramselectname + '\n' + str_line)
        # self.client.get_service_type(self.paramselectname, self.getparamdetailcallback)

    def getparamdetailcallback(self, data):
        # print(data)
        self.m_textparam.AppendText('\ngetparam\n' + self.paramselectname + '\nresult:\n')
        str_line = '-----------------------\n'
        self.m_textparam.AppendText(str_line)
        self.m_textparam.AppendText(str(data)+ '\n')
        self.m_textparam.AppendText(str_line)
        # jsontest = json.dumps(dict(data), sort_keys=True, indent=2, separators=(',', ': '))
        # self.m_textparam.AppendText(jsontest)
        # print(jsontest)

    def setparamdetailcallback(self, data):
        # print(data)
        self.m_textparam.AppendText('\nsetparam\n' + self.paramselectname + '\nresult:\n')
        str_line = '-----------------------\n'
        self.m_textparam.AppendText(str_line)
        self.m_textparam.AppendText(str(data)+ '\n')
        self.m_textparam.AppendText(str_line)

    def OnClickparamget(self, event):
        if self.selectparam:
            self.selectparam.get(self.getparamdetailcallback)
        pass

    def OnClickparamset(self, event):
        if self.selectparam:
            str_value = str(self.m_textparamset.GetValue())
            self.selectparam.set(str_value, self.setparamdetailcallback)
        pass

    def OnClickgetparam(self, event):
        if self.client.is_connected:
            # print('haha')
            self.client.get_params(self.paramcallback)

    def paramcallback(self, data):
        self.m_listBoxparamdetail = data['names']
        self.m_listBoxparam.Clear()
        self.m_listBoxparam.AppendItems(self.m_listBoxparamdetail)

    # 这是severce的地方
    def OnClearservice(self,event):
        self.m_textservice.Clear()

    def OnListBoxSelectservice(self, event):
        index = self.m_listBoxservice.GetSelection()
        self.serviceselectname = self.m_listBoxservicedetail[index]
        self.client.get_service_type(self.serviceselectname,self.getservicedetailcallback)

    def getservicedetailcallback(self, data):
        jsontest = json.dumps(dict(data), sort_keys=True, indent=2, separators=(',', ': '))
        self.m_textservice.AppendText(jsontest)
        # print(jsontest)

    def OnClickgetservice(self,event):
        if self.client.is_connected:
            # print('haha')
            self.client.get_services(self.servicecallback)

    def servicecallback(self, data):
        self.m_listBoxservicedetail = data['services']
        # print(self.m_listBoxservicedetail)
        self.m_listBoxservice.Clear()
        self.m_listBoxservice.AppendItems(self.m_listBoxservicedetail)

    # 这是node的地方
    def OnClearnode(self,event):
        self.m_textnode.Clear()

    def OnListBoxSelect(self, event):
        index = self.m_listBoxnode.GetSelection()
        # print(index)
        self.client.get_node_details(self.m_listBoxnodedetail[index],self.getnodedetailcallback)


    def getnodedetailcallback(self, data):
        jsontest = json.dumps(dict(data), sort_keys=True, indent=2, separators=(',', ': '))
        self.m_textnode.AppendText(jsontest)
        # print(data)

    def OnClickgetnode(self,event):
        if self.client.is_connected:
            # print('haha')
            self.client.get_nodes(self.nodecallback)

    def start_receiving(self, listener, listener_callback):
        listener.subscribe(listener_callback)


    def nodecallback(self,data):
        self.m_listBoxnodedetail = data['nodes']
        # print(self.m_listBoxnodedetail)
        self.m_listBoxnode.Clear()
        self.m_listBoxnode.AppendItems(self.m_listBoxnodedetail)

    def listener_callback(self,data):
        # print(data)
        # json_data = json.loads(str(data))
        # print(data['data'])
        pass

    def OnTextChange(self, event):
        # print('test_ok')
        self.hostname = str(self.m_textCtrlip.GetValue())
        self.hostport = str(self.m_textCtrlport.GetValue())
        # print(self.hostname)
        # print(self.hostport)
        if self.hostname != '' and self.hostport != '' and self.hostport.isdigit() and self.check_ip(self.hostname):
            if 1 < int(self.hostport) < 65535:
                self.m_buttonconnect.Enable(True)
        else:
            self.m_buttonconnect.Enable(False)

    def check_ip(self,ipAddr):
        compile_ip = re.compile(
            '^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|[1-9])\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d'
            '|\\d)\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$')
        if compile_ip.match(ipAddr):
            return True
        else:
            # print(False)
            return False


    def On_Click_connct(self,event):
        if self.m_buttonconnect.GetLabelText() == '连接':
            self.m_checkBox_auto.SetValue(False)
            self.m_texttopicsettime.SetValue('1000')
            self.hostname = str(self.m_textCtrlip.GetValue())
            self.hostport = str(self.m_textCtrlport.GetValue())
            self.client = roslibpy.Ros(host=self.hostname, port=int(self.hostport))
            self.m_buttonconnect.SetLabelText('连接中···')
            self.connect_staus = '连接中'
        elif self.m_buttonconnect.GetLabelText() == '断开':
            self.timer_publish.Stop()
            self.topicsubdict.clear()
            self.m_buttonconnect.SetLabelText('断开中···')
            self.connect_staus = '断开中'

    def OnClickClear(self,event):
        self.m_textCtrlip.SetLabelText('')
        self.m_textCtrlport.SetLabelText('')
        self.hostname = ''
        self.hostport = ''

    def OnCloseWindow(self, event):
        """释放处理"""
        # print('hahahahah')
        self.taskrun = False
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(parent=None)
    frame.Show(True)
    app.MainLoop()
