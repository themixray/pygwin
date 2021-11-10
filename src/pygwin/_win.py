from pygwin.surface import surface as _surface
from pygwin.tray import tray as _tray
from datetime import datetime as _dt
from pygwin.image import save as _s
from pygwin._pg import pg as _pg
import pygwin.image as _img
import win32job as _w32j
import win32api as _w32a
import win32con as _w32c
import win32gui as _w32g
import requests as _req
import tempfile as _tf
import pickle as _p

class win(_surface):
    def __init__(self, iconpath=None):
        self._orig = _pg.display.get_surface()
        super().__init__(self._orig.get_size())
        self._orig = _pg.display.get_surface()
        self._clock = _pg.time.Clock()
        self._withfps = False
        self._iconpath = iconpath
        if iconpath != None:
            self.tray = _tray(self.title,iconpath)
    def update(self, fps=-1):
        if fps != -1:
            self._clock.tick(fps)
            self._withfps = True
        _pg.display.update()
    def title():
        def fget(self):
            return _pg.display.get_caption()[0]
        def fset(self, value):
            if type(value) != str:
                return
            _pg.display.set_caption(value)
        def fdel(self):
            pass
        return locals()
    title = property(**title())
    def icon(value):
        _pg.display.set_icon(_pg.image.load(value))
        self._iconpath = iconpath
    def size():
        def fget(self):
            return _pg.display.get_window_size()
        def fset(self, value):
            if type(value) in [list,tuple]:
                return
            _pg.display.set_mode(value)
        def fdel(self):
            pass
        return locals()
    size = property(**size())
    def fullscreen(self):
        _pg.display.toogle_fullscreen()
    def close(self):
        _pg.display.quit()
        _w32g.PostMessage(self.hwnd, _w32c.WM_CLOSE, 0, 0)
        self.tray.stop()
    def focus(self):
        self.hide()
        self.show()
        _w32g.BringWindowToTop(self.hwnd)
        _w32g.ShowWindow(self.hwnd, _w32c.SW_SHOWNORMAL)
        _w32g.SetForegroundWindow(self.hwnd)
    def unfocus(self):
        pass
    def hide(self):
        _w32g.ShowWindow(self.hwnd, _w32c.SW_HIDE)
    def show(self):
        _w32g.ShowWindow(self.hwnd, _w32c.SW_SHOW)
    def move(self, x, y):
        rect = _w32g.GetWindowRect(self.hwnd)
        _w32g.MoveWindow(self.hwnd, x, y, rect[2]-x, rect[3]-y, 0)
    def screenshot(self, path):
        _s(self._orig, path)
        return path
    @property
    def position(self):
        rect = _w32g.GetWindowRect(self.hwnd)
        x = rect[0]
        y = rect[1]
        return (x, y)
    @property
    def rawFps(self):
        if self._withfps:
            return self._clock.get_fps()
        else:
            return float(f'2010.{_dt.now().year}')
    @property
    def fps(self):
        return int(self.rawFps)
    @property
    def hwnd(self):
        return _pg.display.get_wm_info()['window']
    @property
    def visible(self):
        return _w32g.IsWindowVisible(self._win)

def create(title=None, size=(0,0), icon=None, resizable=False, noframe=False):
    screen = _pg.display.set_mode(size)
    if resizable:
        screen = _pg.display.set_mode(size,_pg.RESIZABLE)
    if noframe:
        screen = _pg.display.set_mode(size,_pg.NOFRAME)
    else:
        if title != None:
            _pg.display.set_caption(title)
        if icon != None:
            _pg.display.set_icon(_pg.image.load(icon))
    return win(icon)

def ramLimit(memory_limit):
    hjob = _w32j.CreateJobObject(None,job_name)
    if breakaway:
        info = _w32j.QueryInformationJobObject(hjob,_w32j.JobObjectExtendedLimitInformation)
        if breakaway=='silent':info['BasicLimitInformation']['LimitFlags']|=(_w32j.JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK)
        else:info['BasicLimitInformation']['LimitFlags']|=(_w32j.JOB_OBJECT_LIMIT_BREAKAWAY_OK)
        _w32j.SetInformationJobObject(hjob,_w32j.JobObjectExtendedLimitInformation,info)
    hprocess = _w32a.GetCurrentProcess()
    try:_w32j.AssignProcessToJobObject(hjob, hprocess);g_hjob=hjob
    except _w32j.error as e:
        if e.winerror!=winerror.ERROR_ACCESS_DENIED:raise
        elif sys.getwindowsversion()>=(6,2):raise
        elif _w32j.IsProcessInJob(hprocess,None):raise
        warnings.warn('The process is already in a job. Nested jobs are not supported prior to Windows 8.')
    info=_w32j.QueryInformationJobObject(g_hjob,_w32j.JobObjectExtendedLimitInformation)
    info['ProcessMemoryLimit']=memory_limit
    info['BasicLimitInformation']['LimitFlags']|=(_w32j.JOB_OBJECT_LIMIT_PROCESS_MEMORY)
    _w32j.SetInformationJobObject(g_hjob,_w32j.JobObjectExtendedLimitInformation,info)

def close():
    _pg.quit()
    quit()

def getEvents():
    return _pg.event.get()
