from pygwin._pg import pg

_aliases = {'w':['width'],'h':['height'],
            'c':['center','middle'],
            'x':['left'],'y':['up'],
            'r':['right'],'d':['down']}

class rect:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._reload()
    def collide(self, x):
        try:return self._rect.colliderect(x._rect_rect)
        except:return self._rect.colliderect(x._rect)
    def contains(self, x, y):
        return self._rect.collidepoint(x,y)
    def copy(self):
        return rect(self.x,self.y,self.w,self.h)
    def _reload(self):
        self.c = (self.x/2+self.w/2,self.y/2+self.h/2)
        self.cx, self.cy = self.c
        self.r,self.d = self.x+self.w,self.y+self.h
        self._rect = pg.Rect(self.x,self.y,self.w,self.h)
    def __getitem__(self,x):
        return [self.x,self.y,self.w,self.h][x]
    def __list__(self):
        return [self.x,self.y,self.w,self.h]
    def __tuple__(self):
        return (self.x,self.y,self.w,self.h)
    def __str__(self):
        return f'<{self.x}x{self.y},{self.w}x{self.h}>'
    def __setattr__(self,attr,data):
        if attr in _aliases.values():
            ma = None
            for i in _aliases.items():
                if i[1] in attr:
                    ma = i[0]
                    break
            attr = ma
        object.__setattr__(self,attr,data)
    def __getattr__(self,attr):
        if attr in _aliases.values():
            ma = None
            for i in _aliases.items():
                if i[1] == attr:
                    ma = i[0]
                    break
            attr = ma
        data = self.__dict__[attr]
        return data


# def fromSurface(surf,x=0,y=0,c=())
#
# # print(dir(property))
# r = rect(123,321,654,987)
# print(r.width)
