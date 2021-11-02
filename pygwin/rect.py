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
    def collide(self, x):
        return pg.Rect(self.x,self.y,self.w,self.h).colliderect(pg.Rect(x.x,x.y,x.w,x.h))
    def contains(self, x, y):
        return pg.Rect(self.x,self.y,self.w,self.h).collidepoint(x,y)
