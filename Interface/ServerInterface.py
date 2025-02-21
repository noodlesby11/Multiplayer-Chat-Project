# coding:utf-8
#服务器端界面
import time

import wx
from socket import socket,AF_INET,SOCK_STREAM
class ServerInterface(wx.Frame):
    def __init__(self):
        #调用父类的初始化方法
        #None；没有父类窗口
        #id:表示当前窗口的编号
        #pos:窗体打开位置
        #size:窗体大小单位是像素
        wx.Frame.__init__(self,None,id=1002,title='多人聊天室服务器端',pos=wx.DefaultPosition,size=(400,450))
        #窗口放一个面板
        pl=wx.Panel(self)
        # 在面板上放盒子,垂直方向布局
        box = wx.BoxSizer(wx.VERTICAL)
        # 可伸缩的网格布局,水平方向布局
        fgz1 = wx.FlexGridSizer(wx.HSCROLL)

        # 创建按钮
        start_server_btn = wx.Button(pl, size=(133, 40), label='启动服务')
        record_btn = wx.Button(pl, size=(133, 40), label='保存聊天记录')
        stop_server_btn = wx.Button(pl, size=(133, 40), label='停止服务')

        # 把两个按钮放到可伸缩的网格布局
        fgz1.Add(start_server_btn, 1, wx.Top)
        fgz1.Add(record_btn, 1, wx.Top)
        fgz1.Add(stop_server_btn, 1, wx.Top)
        box.Add(fgz1, 1, wx.ALIGN_CENTRE)

        #只读文本显示聊天内容
        self.show_text=wx.TextCtrl(pl,size=(400,410),style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.show_text,1,wx.ALIGN_CENTER)

        pl.SetSizer(box)

        """设置服务器属性"""
        self.isOn=False#存储服务器启动状态
        self.host_port=('',8888)#空字符串代表所有本机IP
        self.server_socket=socket(AF_INET,SOCK_STREAM)#创建socket对象
        self.server_socket.bind(self.host_port)#绑定IP地址和端口
        self.server_socket.listen(5)#监听
        self.session_thread_dict={}#存储客户端对话和会话线程的字典

        #绑定鼠标事件
        self.Bind(wx.EVT_BUTTON,self.start_server,start_server_btn)

    def start_server(self,event):
        print("服务器启动")

if __name__ =='__main__':
    app=wx.App()
    client=ServerInterface()
    client.Show()
    #循环刷新显示
    app.MainLoop()