from pygwin.rect import rect as _r
from pygwin._pg import pg as _pg

class surface:
    def __init__(self, size):
        self._size = size
        self._orig = _pg.Surface(size, _pg.SRCALPHA)
    @property
    def pixels(self):
        pixels = []
        pxls = _pg.PixelArray(self._orig)
        for x in range(self.size[0]):
            pixels.append([])
            for y in range(self.size[1]):
                pixels[x].append(pxls[x, y])
        return pixels
    @property
    def size(self):
        return self._size
    def rect(self, x=0, y=0, center=[]):
        if center == []:
            return _r(x, y, self.size[0], self.size[1])
        else:
            return _r(center[0]-(self.size[0]/2),
                      center[1]-(self.size[1]/2),
                      self.size[0], self.size[1])
    def copy(self):
        surf = surface(self._size)
        surf._surface_orig = self._orig
        surf._surface_size = self._size
        return surf
    def getPixel(self, x, y):
        return self._orig.get_at((x,y))
    def setPixel(self, x, y, color):
        self._orig.set_at((x,y),color)
        return self.copy()
    def blit(self, surf, xy):
        if type(surf) != surface:
            from pygwin.font import defaultFont as _df
            surf = _df.render(surf, 25, (0,0,0))
        try:
            self._orig.blit(surf._surface_orig, xy)
        except:
            self._orig.blit(surf._orig, xy)
        return self.copy()
    def fill(self, color):
        self._orig.fill(color)
        return self.copy()
    def crop(self, rect):
        self._orig = self._orig.subsurface((rect.x,rect.y,rect.w,rect.h))
        self._size = self._orig.get_size()
        return self.copy()
    def scale(self, rect):
        self._orig = _pg.transform.scale(self._orig, (rect.w, rect.h))
        self._size = self._orig.get_size()
        return self.copy()
    def rotate(self, angle):
        self._orig = _pg.transform.rotate(self._orig, angle)
        self._size = self._orig.get_size()
        return self.copy()
    def flip(self, x, y):
        self._orig = _pg.transform.flip(self._orig, x, y)
        return self.copy()
    def blur(self, amt):
        if amt < 0:
            return self.copy()
        scale = (int(self._orig.get_width()*(amt+1)),int(self._orig.get_height()[1]*(amt+1)))
        size = self._orig.get_size()
        self._orig = _pg.transform.smoothscale(self._orig,scale)
        self._orig = _pg.transform.smoothscale(self._orig,size)
        return self.copy()
    class _draw:
        def __init__(self,surface):
            self._surf = surface
        def rect(self,color,rect,
                 width=0,borderRadius=0,
                 borderTopLeftRadius=-1,
                 borderTopRightRadius=-1,
                 borderBottomLeftRadius=-1,
                 borderBottomRightRadius=-1):
            try:
                orig = self._surf._surface_orig
            except:
                orig = self._surf._orig
            _pg.draw.rect(orig,color,_pg.Rect(rect.x,rect.y,rect.w,rect.h),
                         width,borderRadius,borderTopLeftRadius,
                         borderTopRightRadius,borderBottomLeftRadius,
                         borderBottomRightRadius)
            return self._surf.copy()
        def polygon(self, color, points, width=0):
            try:
                orig = self._surf._surface_orig
            except:
                orig = self._surf._orig
            _pg.draw.polygon(orig,color,points,width)
            return self._surf.copy()
        def circle(self,color,center,
                   radius,width=0,
                   drawTopLeft=1,
                   drawTopRight=1,
                   drawBottomLeft=1,
                   drawBottomRight=1):
            try:
                orig = self._surf._surface_orig
            except:
                orig = self._surf._orig
            _pg.draw.circle(orig,color,center,radius,
                            width,drawTopRight,drawTopLeft,
                            drawBottomLeft,drawBottomRight)
            return self._surf.copy()
        def ellipse(self,color,rect,width=0):
            try:
                orig = self._surf._surface_orig
            except:
                orig = self._surf._orig
            _pg.draw.ellipse(orig,color,_pg.Rect(rect.x,rect.y,rect.w,rect.h),width)
            return self._surf.copy()
        def line(self,color,start,end,width=1):
            try:
                orig = self._surf._surface_orig
            except:
                orig = self._surf._orig
            _pg.draw.line(orig,color,start,end,width)
            return self._surf.copy()
        def arc(self,color,rect,startAngle,stopAngle,width=1):
            try:
                orig = self._surf._surface_orig
            except:
                orig = self._surf._orig
            _pg.draw.arc(orig,color,
                        _pg.Rect(rect.x,rect.y,rect.w,rect.h),
                        startAngle,stopAngle,width)
            return self._surf.copy()
    @property
    def draw(self):
        return self._draw(self)
