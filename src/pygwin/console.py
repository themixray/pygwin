from pygwin._pg import pg
try:
    import win32console as w32con
    import win32con as w32c
    import win32gui as w32g
    import win32api as w32a
    nonwin32api = True
except:
    nonwin32api = False
import pyautogui as pag

class console:
    def __init__(self):
        if not nonwin32api:
            self._hwnd = w32con.GetConsoleWindow()
    @property
    def hwnd(self):
        if not nonwin32api:
            return self._hwnd
    def focus(self):
        if not nonwin32api:
            self.hide()
            self.show()
            w32g.BringWindowToTop(self.hwnd)
            w32g.ShowWindow(self.hwnd, w32c.SW_SHOWNORMAL)
            w32g.SetForegroundWindow(self.hwnd)
    def hide(self):
        if not nonwin32api:
            w32g.ShowWindow(self.hwnd, w32c.SW_HIDE)
    def show(self):
        if not nonwin32api:
            w32g.ShowWindow(self.hwnd, w32c.SW_SHOW)
    def move(self, x, y):
        if not nonwin32api:
            w32g.SetWindowPos(self.hwnd, x, y, self.size[0], self.size[1])
    def resize(self, width, height):
        if not nonwin32api:
            w32g.SetWindowPos(self.hwnd, self.position[0], self.position[1], width, height)
    def minimize(self):
        if not nonwin32api:
            w32g.ShowWindow(hwnd, w32c.SW_MINIMIZE)
            return self.size
    def maximize(self):
        if not nonwin32api:
            w32g.ShowWindow(hwnd, w32c.SW_MAXIMIZE)
            return self.size
    def title():
        def fget(self):
            if not nonwin32api:
                return w32con.GetConsoleTitle()
        def fset(self, value):
            if not nonwin32api:
                w32con.SetConsoleTitle(str(value))
        def fdel(self):
            pass
        return locals()
    title = property(**title())
    def center(self,x=_pg.display.get_desktop_sizes()[0][0]/2,
                    y=_pg.display.get_desktop_sizes()[0][1]/2):
        if not nonwin32api:
            self.move(x-self.size[0]/2,y-self.size[1]/2)
    @property
    def visible(self):
        if not nonwin32api:
            return w32g.IsWindowVisible(self.hwnd)
    @property
    def position(self):
        if not nonwin32api:
            rect = w32g.GetWindowRect(self.hwnd)
            x = rect[0]+7
            y = rect[1]
            return (x, y)
    @property
    def size(self):
        if not nonwin32api:
            rect = w32g.GetWindowRect(self.hwnd)
            w = rect[2] - self.position[0]-7
            h = rect[3] - self.position[1]-7
            return (w, h)
    def screenshot(self, path):
        if not nonwin32api:
            rect = self.position+self.size
            self.focus()
            pag.screenshot(path, region=rect)
            return path
console = console()
