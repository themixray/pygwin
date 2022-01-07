from pygwin.surface import surface as _surface
from pygwin.tray import tray as _tray
from datetime import datetime as _dt
from pygwin.image import save as _s
from pygwin._pg import pg as _pg
import pygwin.image as _img
try:
    import win32job as _w32j
    import win32api as _w32a
    import win32con as _w32c
    import win32gui as _w32g
    nonwin32api = False
except:
    nonwin32api = True
import sys as _sys
import warnings as _warn
import winerror as _we
import requests as _req
import tempfile as _tf
import threading as _t
import pickle as _p
import mouse as _m
import time as _ti

class _win(_surface):
    def __init__(self, iconpath=None):
        self._orig = _pg.display.get_surface()
        super().__init__(self._orig.get_size())
        self._orig = _pg.display.get_surface()
        self._clock = _pg.time.Clock()
        self._withfps = False
        self._iconpath = iconpath
        self._isallowdrag = False
        # self._issmartdrag = False
        if iconpath != None:
            self.tray = _tray(self.title,iconpath)
    def update(self, fps=-1):
        if fps != -1:
            self._clock.tick(fps)
            self._withfps = True
        _pg.display.update()
    def resize(self, size=None):
        if size == None:
            return self.size
        else:
            self._orig = _pg.display.set_mode(size)
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
        # _w32g.PostMessage(self.hwnd, _w32c.WM_CLOSE, 0, 0)
        _pg.display.quit()
        try:self.tray.stop()
        except:pass
    def focus(self):
        if not nonwin32api:
            self.hide()
            self.show()
            _w32g.BringWindowToTop(self.hwnd)
            _w32g.ShowWindow(self.hwnd, _w32c.SW_SHOWNORMAL)
            _w32g.SetForegroundWindow(self.hwnd)
    def hide(self):
        if not nonwin32api:
            _w32g.ShowWindow(self.hwnd, _w32c.SW_HIDE)
    def show(self):
        if not nonwin32api:
            _w32g.ShowWindow(self.hwnd, _w32c.SW_SHOW)
    def move(self, x, y):
        if not nonwin32api:
            rect = self._getRect()
            _w32g.MoveWindow(self.hwnd, int(x), int(y),
                             rect[2]-x, rect[3]-y, 0)
    def screenshot(self, path):
        _s(self._orig, path)
        return path
    def center(self,x=_pg.display.get_desktop_sizes()[0][0]/2,
                    y=_pg.display.get_desktop_sizes()[0][1]/2):
        self.move(x-self.size[0]/2,y-self.size[1]/2)
    def _getRect(self):
        if not nonwin32api:
            return _w32g.GetWindowRect(self.hwnd)
    def denyDrag(self):
        if not nonwin32api:
            self._isallowdrag = True
            def loop(self):
                while self._isallowdrag:
                    pos = _m.get_position()
                    pos = [pos[i]-self.position[i] for i in range(2)]
                    if pos[0] < self._getRect()[2]-137:
                        if pos[1] < 30:
                            _m.release('left')
            _t.Thread(target=lambda:loop(self),daemon=1).start()
    def allowDrag(self):
        if not nonwin32api:
            self._isallowdrag = False
    # def smartDrag(self, x):
    #     self.allowDrag()
    #     self._issmartdrag = x
    #     if x:
    #         self._isallowdrag = True
    #         def loop(self):
    #             wsd = None
    #             while self._issmartdrag:
    #                 self.update()
    #                 pos = _m.get_position()
    #                 pos = [pos[i]-self.position[i] for i in range(2)]
    #                 if pos[0] < _w32g.GetWindowRect(self.hwnd)[2]-137:
    #                     if pos[1] < 30:
    #                         if _m.is_pressed('left'):
    #                             _m.release('left')
    #                             if wsd == None:
    #                                 wsd = pos+list(self.position)
    #                             else:
    #                                 if wsd != pos+list(self.position):
    #                                     self.move(wsd[2]+(pos[0]-wsd[0]),
    #                                               wsd[3]+(pos[1]-wsd[1]))
    #                         else:
    #                             wsd = None
    #                 _ti.sleep(0.5)
    #         _t.Thread(target=lambda:loop(self),daemon=1).start()
    @property
    def position(self):
        if not nonwin32api:
            rect = self._getRect()
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
        if not nonwin32api:
            return _pg.display.get_wm_info()['window']
    @property
    def visible(self):
        if not nonwin32api:
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
    return _win(icon)

def ramLimit(memory_limit):
    if not nonwin32api:
        g_hjob = None
        def create_job(job_name='', breakaway='silent'):
            hjob = _w32j.CreateJobObject(None, job_name)
            if breakaway:
                info = _w32j.QueryInformationJobObject(hjob,
                            _w32j.JobObjectExtendedLimitInformation)
                if breakaway == 'silent':
                    info['BasicLimitInformation']['LimitFlags'] |= (
                        _w32j.JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK)
                else:
                    info['BasicLimitInformation']['LimitFlags'] |= (
                        _w32j.JOB_OBJECT_LIMIT_BREAKAWAY_OK)
                _w32j.SetInformationJobObject(hjob,
                    _w32j.JobObjectExtendedLimitInformation, info)
            return hjob
        def assign_job(hjob):
            global g_hjob
            hprocess = _w32a.GetCurrentProcess()
            try:
                _w32j.AssignProcessToJobObject(hjob, hprocess)
                g_hjob = hjob
            except _w32j.error as e:
                if (e._we != _we.ERROR_ACCESS_DENIED or
                    _sys.getwindowsversion() >= (6, 2) or
                    not _w32j.IsProcessInJob(hprocess, None)):
                    raise
                _warn.warn('The process is already in a job. Nested jobs are not '
                    'supported prior to Windows 8.')
        def limit_memory(memory_limit):
            if g_hjob is None:
                return
            info = _w32j.QueryInformationJobObject(g_hjob,
                        _w32j.JobObjectExtendedLimitInformation)
            info['ProcessMemoryLimit'] = memory_limit
            info['BasicLimitInformation']['LimitFlags'] |= (
                _w32j.JOB_OBJECT_LIMIT_PROCESS_MEMORY)
            _w32j.SetInformationJobObject(g_hjob,
                _w32j.JobObjectExtendedLimitInformation, info)
        assign_job(create_job())
        limit_memory(memory_limit)

def close():
    _pg.quit()
    quit()

def getEvents():
    return _pg.event.get()
