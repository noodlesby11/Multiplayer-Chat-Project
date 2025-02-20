# coding:utf-8
#服务器端界面
import wx
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

if __name__ =='__main__':
    app=wx.App()
    client=ServerInterface()
    client.Show()
    #循环刷新显示
    app.MainLoop()