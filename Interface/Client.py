# coding:utf-8
#用户端界面
import socket
import threading
import wx

class ClientInterface(wx.Frame):
    def __init__(self,client_name):
        #调用父类的初始化方法
        #None；没有父类窗口
        #id:表示当前窗口的编号
        #pos:窗体打开位置
        #size:窗体大小单位是像素
        wx.Frame.__init__(self,None,id=1001,title=client_name+' 的客户端界面',pos=wx.DefaultPosition,size=(400,450))
        #创建面板对象
        pl=wx.Panel(self)
        #在面板上放盒子,垂直方向布局
        box=wx.BoxSizer(wx.VERTICAL)
        #可伸缩的网格布局,水平方向布局
        fgz1=wx.FlexGridSizer(wx.HSCROLL)

        #创建两个按钮
        conn_btn=wx.Button(pl,size=(200,40),label='连接')
        dis_conn_btn=wx.Button(pl,size=(200,40),label='断开')

        #把两个按钮放到可伸缩的网格布局
        fgz1.Add(conn_btn,1,wx.Top|wx.LEFT)
        fgz1.Add(dis_conn_btn,1,wx.Top|wx.RIGHT)
        box.Add(fgz1,1,wx.ALIGN_CENTRE)

        #只读文本显示聊天内容
        self.show_text=wx.TextCtrl(pl,size=(400,210),style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.show_text,1,wx.ALIGN_CENTER)

        #创建聊天内容的文本框
        self.chat_text = wx.TextCtrl(pl, size=(400, 120), style=wx.TE_MULTILINE)
        box.Add(self.chat_text, 1, wx.ALIGN_CENTER)

        #可伸缩的网格布局
        fgz2=wx.FlexGridSizer(wx.HSCROLL)
        #创建两个按钮
        reset_btn = wx.Button(pl, size=(200, 40), label='重置')
        send_btn = wx.Button(pl, size=(200, 40), label='发送')


        # 把两个按钮放到可伸缩的网格布局
        fgz2.Add(reset_btn, 1, wx.Top | wx.LEFT)
        fgz2.Add(send_btn, 1, wx.Top | wx.LEFT)
        box.Add(fgz2, 1, wx.ALIGN_CENTRE)

        #将盒子放到面板中
        pl.SetSizer(box)

        """----------------------设置客户端属性-------------------------"""
        self.Bind(wx.EVT_BUTTON,self.connect_to_server,conn_btn)#连接按钮事件
        self.Bind(wx.EVT_BUTTON, self.send_to_server,send_btn)#发送按钮事件
        self.Bind(wx.EVT_BUTTON, self.dis_conn_server,dis_conn_btn)#断开按钮事件
        self.Bind(wx.EVT_BUTTON, self.reset,reset_btn)#重置按钮事件
        #实例属性的设置
        self.client_name=client_name
        self.isConnected=False#客户端连接状态
        self.client_socket=None#设置客户端socket
    #连接按钮事件
    def connect_to_server(self,event):
        print(f'[{self.client_name}]已登录')
        if not self.isConnected:
            server_host_port=('127.0.0.1',8888)
            #创建socket对象
            self.client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #发送连接请求
            self.client_socket.connect(server_host_port)
            #只要连接成功久发送一条数据
            self.client_socket.send(self.client_name.encode('utf-8'))
            #启动一个线程，客户端线程与服务端线程进行会话
            client_thread=threading.Thread(target=self.recv_data)
            #设置成守护线程，即窗体关掉子线程也会关闭
            client_thread.daemon=True
            #修改连接状态
            self.isConnected=True
            #启动线程
            client_thread.start()
    #发送按钮事件
    def send_to_server(self,event):
        if self.isConnected:
            #从文本框中获取数据
            input_data=self.chat_text.GetValue()
            if input_data!='':
                #向服务器发送数据
                self.client_socket.send(input_data.encode('utf-8'))
                #清空文本框
                self.chat_text.SetValue('')
    #断开按钮事件
    def dis_conn_server(self,event):
        #发送断开信息
        self.client_socket.send('Disconnect-S'.encode('utf-8'))
        self.isConnected=False
        #客户端显示断开信息
        self.show_text.AppendText('-' * 40 + '\n')
        self.show_text.AppendText('你已断开连接\n')
    #重置按钮事件
    def reset(self,event):
        #清空输入文本框
        self.chat_text.Clear()
    #接收服务器的信息
    def recv_data(self):
        while self.isConnected:
            #接收来自服务器的数据
            data=self.client_socket.recv(1024).decode('utf-8')
            #显示到可读文本框中
            self.show_text.AppendText('-'*40+'\n'+data+'\n')


if __name__ =='__main__':
    app=wx.App()
    name=input('请输入名称:')
    client=ClientInterface(name)
    client.Show()
    #循环刷新显示
    app.MainLoop()