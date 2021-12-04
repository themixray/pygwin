import win32console as w32con
import win32con as w32c
import win32gui as w32g
import pyautogui as pag

class console:
    def __init__(self):
        self._hwnd = w32con.GetConsoleWindow()
    @property
    def hwnd(self):
        return self._hwnd
    def focus(self):
        self.hide()
        self.show()
        w32g.BringWindowToTop(self.hwnd)
        w32g.ShowWindow(self.hwnd, w32c.SW_SHOWNORMAL)
        w32g.SetForegroundWindow(self.hwnd)
    def unfocus(self):
        pass
    def hide(self):
        w32g.ShowWindow(self.hwnd, w32c.SW_HIDE)
    def show(self):
        w32g.ShowWindow(self.hwnd, w32c.SW_SHOW)
    def move(self, x, y):
        w32g.SetWindowPos(self.hwnd, x, y, self.size[0], self.size[1])
    def resize(self, width, height):
        w32g.SetWindowPos(self.hwnd, self.position[0], self.position[1], width, height)
    def minimize(self):
        w32g.ShowWindow(hwnd, w32c.SW_MINIMIZE)
        return self.size
    def maximize(self):
        w32g.ShowWindow(hwnd, w32c.SW_MAXIMIZE)
        return self.size
    def title():
        def fget(self):
            return w32con.GetConsoleTitle()
        def fset(self, value):
            w32con.SetConsoleTitle(str(value))
        def fdel(self):
            pass
        return locals()
    title = property(**title())
    @property
    def visible(self):
        return w32g.IsWindowVisible(self.hwnd)
    @property
    def position(self):
        rect = w32g.GetWindowRect(self.hwnd)
        x = rect[0]+7
        y = rect[1]
        return (x, y)
    @property
    def size(self):
        rect = w32g.GetWindowRect(self.hwnd)
        w = rect[2] - self.position[0]-7
        h = rect[3] - self.position[1]-7
        return (w, h)
    def screenshot(self, path):
        rect = self.position+self.size
        self.focus()
        pag.screenshot(path, region=rect)
        return path
console = console()
