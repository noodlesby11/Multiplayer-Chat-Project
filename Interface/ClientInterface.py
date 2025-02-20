# coding:utf-8
#用户端界面
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
        self.chat_text = wx.TextCtrl(pl, size=(400, 120), style=wx.TE_MULTILINE | wx.TE_READONLY)
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

if __name__ =='__main__':
    app=wx.App()
    client=ClientInterface('测试用户')
    client.Show()
    #循环刷新显示
    app.MainLoop()