from pygwin.surface import surface as _surface
from pygwin._pg import pg as _pg

class font:
    def __init__(self, path):
        self._path = path
    def _font(self, size):
        return _pg.font.Font(self._path,size)
    def render(self, text, size, color, newLineSpace=5,
               italic=False, bold=False, underline=False):
        text = str(text)
        font = self._font(size)
        font.set_italic(italic)
        font.set_bold(bold)
        font.set_underline(underline)
        if text.replace('\n', '') != text:
            text = text.split('\n')
            surf = _pg.Surface([font.size(max(text,key=lambda x:font.size(x)[0]))[0],
                                (font.size('123')[1]+newLineSpace)*len(text)],_pg.SRCALPHA)
            y = 0
            for i in text:
                r = font.render(i, True, color)
                surf.blit(r, (0, y))
                y += font.size(i)[1]
                if i != text[-1]:
                    y += newLineSpace
        else:
            surf = font.render(text, True, color)
        surface = _surface(surf.get_size())
        surface._surface_orig = surf
        return surface
    def size(self, text, size, newLineSpace=5,
             italic=False,bold=False,underline=False):
        return self.render(text, size, (255,255,255),
                           newLineSpace=newLineSpace,
                           italic=italic, bold=bold,
                           underline=underline).size

class sysFont(font):
    def __init__(self, name):
        self._path = _pg.font.match_font(name)

defaultFont = font(_pg.font.get_default_font())
