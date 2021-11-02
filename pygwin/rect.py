from pygwin._pg import pg

class rect:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
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
    def contains(self, xorect, y=None):
        if type(xorect) == rect and y == None:
            return pg.Rect(self.x,self.y,
            self.w,self.h).contains(pg.Rect(
            xorect.x,xorect.y,xorect.w,xorect.h))
        elif type(xorect) != rect and y != None:
            return pg.Rect(self.x,self.y,self.w,
            self.h).collidepoint((xorect,y))
