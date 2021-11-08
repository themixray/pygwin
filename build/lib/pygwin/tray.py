import threading
import wx
import wx.adv
from pygwin._pg import pg
import copy

class tray(wx.adv.TaskBarIcon):
    def __init__(self, tooltip, iconpath):
        class App(wx.App):
            def OnInit(self):
                self.frame = wx.Frame(None)
                self.SetTopWindow(self.frame)
                return True
        self._app = App(False)
        self.frame = self._app.frame
        super().__init__()
        self._tooltip = tooltip
        self._iconpath = iconpath
        self.setIcon(iconpath)
        self._menu = wx.Menu()
    def CreatePopupMenu(self):
        return self._menu
    def GetPopupMenu(self):
        return self._menu
    def setIcon(self, path):
        self._bicon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(self._bicon, self._tooltip)
    def setTooltip(self, tooltip):
        self.SetIcon(self._bicon, tooltip)
        self._tooltip = tooltip
    def onLeftMouseButton(self):
        pass
    def addSeparator(self):
        self._menu.AppendSeparator()
    def addCommand(self,text,func=lambda:None):
        item = wx.MenuItem(self._menu,-1,text)
        self._menu.Bind(wx.EVT_MENU,
                        lambda x:func(),
                        id=item.GetId())
        self._menu.Append(item)
    def start(self, thread=True):
        cbotld = lambda x:self.onLeftMouseButton()
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN,cbotld)
        if thread: threading.Thread(
            target=self._app.MainLoop,
            daemon=1).start()
        else: self._app.MainLoop()
    def stop(self):
        wx.CallAfter(self._app.frame.Close)
