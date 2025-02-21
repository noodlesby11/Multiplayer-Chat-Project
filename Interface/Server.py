# coding:utf-8
#服务器端界面
import threading
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

        """----------------------设置服务器属性-------------------------"""
        self.isOn=False#存储服务器启动状态
        self.host_port=('',8888)#空字符串代表所有本机IP
        self.server_socket=socket(AF_INET,SOCK_STREAM)#创建socket对象
        self.server_socket.bind(self.host_port)#绑定IP地址和端口
        self.server_socket.listen(5)#监听
        self.session_thread_dict={}#存储客户端对话和会话线程的字典

        #绑定 启动服务 按钮事件
        self.Bind(wx.EVT_BUTTON,self.start_server,start_server_btn)
        #绑定 保存聊天 按钮事件
        self.Bind(wx.EVT_BUTTON,self.save_record,record_btn)
        #绑定 停止服务 按钮事件
        self.Bind(wx.EVT_BUTTON,self.stop_server,stop_server_btn)
    #启动服务 按钮事件
    def start_server(self,event):
        if not self.isOn:
            #启动服务器
            self.isOn=True
            #创建主线程对象，函数式创建主线程
            main_thread=threading.Thread(target=self.do_work)
            #设置为守护线程，父线程执行结束子线程也结束
            main_thread.daemon=True
            #启动主线程
            main_thread.start()
    #保存聊天 按钮事件
    def save_record(self,event):
        record_data=self.show_text.GetValue()
        with open('record.log','w',encoding='utf-8') as file:
            file.write(record_data)
        self.show_text.AppendText('-' * 40 + '\n')
        self.show_text.AppendText('聊天记录已保存\n')
    #停止服务 按钮事件
    def stop_server(self,event):
        print('服务器停止服务')
        self.isOn = False
    #主线程函数
    def do_work(self):
        while self.isOn:
            #接收客户端的连接请求
            session_socket,client_addr=self.server_socket.accept()
            #客户端发送连接请求后，发送过来的第一条数据为客户端名称，将此作为字典中的键
            user_name=session_socket.recv(1024).decode('utf-8')
            #创建一个会话线程对象
            session_thread=SessionThread(session_socket,user_name,self)
            #存储到字典中
            self.session_thread_dict[user_name]=session_thread
            #启动会话线程
            session_thread.start()
            #输出服务器的提示信息
            self.show_info_and_send_client('服务器通知',f'{user_name}进入聊天室',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
        #当self.isOn==false执行关闭socket对象
        self.server_socket.close()
    #显示信息
    def show_info_and_send_client(self,data_source,data,data_time):
        #字符串操作
        send_data=f'{data_source}:{data}\n{data_time}'
        #显示在只读文本框
        self.show_text.AppendText('-'*40+'\n'+send_data+'\n')
        #每个客户端都发送一次
        for c in self.session_thread_dict.values():
            if c.isOn:
                c.client_socket.send(send_data.encode('utf-8'))

#服务器会话线程的类
class SessionThread(threading.Thread):
    def __init__(self,client_socket,user_name,server):
        #调用父类的初始化方法
        threading.Thread.__init__(self)
        self.client_socket=client_socket
        self.user_name=user_name
        self.server=server
        #会话线程在这里进行启动
        self.isOn=True

    def run(self)->None:
        print(f'客户端:[{self.user_name}]已经和服务器连接成功')
        while self.isOn:
            #从客户端接收数据 存储到data中
            data=self.client_socket.recv(1024).decode('utf-8')
            #客户端点击断开连接，先发送一句话，自定义
            if data=='Disconnect-S':
                self.isOn=False
                #发送断开通知
                self.server.show_info_and_send_client('服务器通知', f'{self.user_name}离开聊天室',
                                               time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            else:
                #若为其他消息则显示给所有客户端，包含服务器
                self.server.show_info_and_send_client(self.user_name,data,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
        #关闭
        self.client_socket.close()

if __name__ =='__main__':
    app=wx.App()
    client=ServerInterface()
    client.Show()
    #循环刷新显示
    app.MainLoop()