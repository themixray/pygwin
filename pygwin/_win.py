from pygwin.surface import surface as _surface
from datetime import datetime as _dt
from pygwin._pg import pg as _pg
import win32job as _w32j
import win32api as _w32a

class win(_surface):
    def __init__(self):
        self._orig = _pg.display.get_surface()
        super().__init__(self._orig.get_size())
        self._orig = _pg.display.get_surface()
        self._clock = _pg.time.Clock()
        self._withfps = False
    def update(self, fps=-1):
        if fps != -1:
            self._clock.tick(fps)
            self._withfps = True
        _pg.display.update()
    def title():
        def fget(self):
            return _pg.display.get_caption()
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
    def size():
        def fget(self):
            return _pg.display.get_window_size()
        def fset(self, value):
            if type(value) != tuple or type(value) != list:
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

def create(title=None, size=(0,0), icon=None):
    screen = _pg.display.set_mode(size)
    if title != None: _pg.display.set_caption(title)
    if icon != None: _pg.display.set_icon(_pg.image.load(icon))
    return win()

def ramLimit(bytes):
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
            if (e.winerror != winerror.ERROR_ACCESS_DENIED or
                sys.getwindowsversion() >= (6, 2) or
                not _w32j.IsProcessInJob(hprocess, None)):
                raise
            warnings.warn('The process is already in a job. Nested jobs are not '
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
    limit_memory(bytes)

def close():
    _pg.quit()
    quit()

def getEvents():
    return _pg.event.get()
