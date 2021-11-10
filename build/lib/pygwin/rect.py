from pygwin._pg import pg

class rect:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._rect = pg.Rect(x,y,w,h)
    def width():
        def fget(self):
            return self.w
        def fset(self, value):
            self.w = value
        def fdel(self):
            pass
        return locals()
    width = property(**width())
    def height():
        def fget(self):
            return self.h
        def fset(self, value):
            self.h = value
        def fdel(self):
            pass
        return locals()
    height = property(**height())
    def collide(self, x):
        try:
            return self._rect.colliderect(x._rect_rect)
        except:
            return self._rect.colliderect(x._rect)
    def contains(self, x, y):
        return self._rect.collidepoint(x,y)
