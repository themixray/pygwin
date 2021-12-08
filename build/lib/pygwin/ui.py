from pygwin._pg import pg as _pg
from pygwin.surface import surface as _s
from pygwin.font import defaultFont as _df
from pygwin.image import load as _l
from pygwin.rect import rect as _r
import pygwin.mouse as _m
import pygwin.keyboard as _k
import ctypes as _ct
import copy as _copy

class widget:
    power = True
    destroyed = False
    def _args(self, locals):
        args = _copy.copy(locals)
        for i in args.items():
            if i[0] != 'self':
                exec(f'self.{i[0]} = args["{i[0]}"]')
        self._args = args
    def __init__(self, surface):
        self._args(locals())
    def draw(self, win, pos):
        win.blit(self.surface,pos)
    def on(self):
        self.power = True
    def off(self):
        self.power = False
    def destroy(self):
        self.destroyed = True
    def config(self, **parameters):
        if parameters != {}:
            for i in parameters.items():
                if i[0] in list(self.__dict__.keys()):
                    exec(f'self.{i[0]} = parameters["{i[0]}"]')
                    self._args[i[0]] = i[1]
        else:
            return self._args
        self.__init__(**self._args)
class button(widget):
    def __init__(self,text,
                 func=lambda:None,
                 fontSize=30,font=_df,
                 width=None,height=None,
                 bg=(70,70,70),fg=(180,180,200),
                 afg=(50,50,50),abg=(200,200,200),
                 borderColor=(50,50,50),borderWidth=5):
        super()._args(locals())
        self.cl0 = False
        self.cl1 = False
        self.nc0 = True
        self._generate()
    def _generate(self, position=None):
        if self.width == None or self.height == None:
            textSize = self.font.size(self.text,self.fontSize)
            if self.width != None:
                self.surface = _s((self.width,textSize[1]+10))
            elif self.height != None:
                self.surface = _s((textSize[0]+50,self.height))
            else:
                self.surface = _s((textSize[0]+50,textSize[1]+10))
        else:
            self.surface = _s((self.width,self.height))
        if position != None:
            contains = self.surface.rect(position[0], position[1]).contains(
                                    _m.getPosition()[0], _m.getPosition()[1])
            cacm = contains and _m.isPressed('left')
        else:
            contains = False
            cacm = False
        if contains and not self.cl0:
            _m.setCursor(_pg.SYSTEM_CURSOR_HAND)
            self.cl0 = True
            self.nc0 = True
        elif not contains:
            if self.nc0:
                _m.setCursor(_pg.SYSTEM_CURSOR_ARROW)
                self.nc0 = False
            self.cl0 = False
        if cacm and not self.cl1:
            self.func()
            self.cl1 = True
        elif not cacm:
            self.cl1 = False
        self.surface.fill(self.borderColor)
        if cacm:
            self.surface.draw.rect(self.abg,_r(self.borderWidth,self.borderWidth,
                                self.surface.size[0]-self.borderWidth*2,
                                self.surface.size[1]-self.borderWidth*2))
        else:
            self.surface.draw.rect(self.bg,_r(self.borderWidth,self.borderWidth,
                                self.surface.size[0]-self.borderWidth*2,
                                self.surface.size[1]-self.borderWidth*2))
        if cacm:
            text = self.font.render(self.text,self.fontSize,self.afg)
        else:
            text = self.font.render(self.text,self.fontSize,self.fg)
        pos = text.rect(center=(
                self.surface.size[0]/2,
                self.surface.size[1]/2))
        pos = [pos.x, pos.y]
        self.surface.blit(text,pos)
    def draw(self, win, pos):
        self._generate(pos)
        win.blit(self.surface,pos)
class label(widget):
    def __init__(self,text,size=30,
                 color=(0,0,0),font=_df):
        self.surface = font.render(text,size,color)
class entry(widget):
    def __init__(self,hint='',fontSize=30,font=_df,
                 width=None,height=None,
                 bg=(70,70,70),fg=(180,180,200),
                 afg=(200,200,200),abg=(50,50,50),
                 hintColor=(100,100,100),
                 lineColor=(200,200,200),
                 borderColor=(50,50,50),
                 borderWidth=5,maxSymbols=None,
                 whitelist=None,blacklist=[]):
        super()._args(locals())
        self.text = ''
        self.focus = False
        self.tick = 0
        self.wcl = False
        self.startHint = self.hint
        self.ws = False
        if self.width == None or self.height == None:
            if self.hint != '':
                hintSize = self.font.size(self.hint,self.fontSize)
            else:
                hintSize = (150,self.font.size('X',self.fontSize)[1])
            if self.height == None:
                self.height = hintSize[1]+10
            if self.width == None:
                self.width = hintSize[0]+50
        self.surface = _s((self.width,self.height))
        self.wclk = []
        self.wsnr = False
    def _generate(self,position=None):
        self.surface.fill(self.borderColor)
        if self.focus:
            self.surface.draw.rect(self.abg,_r(self.borderWidth,self.borderWidth,
                                self.surface.size[0]-self.borderWidth*2,
                                self.surface.size[1]-self.borderWidth*2))
            if self.text == '':
                text = self.font.render(self.hint,self.fontSize,self.hintColor)
            else:
                text = self.font.render(self.text,self.fontSize,self.afg)
            x = 10
            if text.size[0] >= self.surface.size[0]-20:
                x = self.surface.size[0]-text.size[0]-10
            self.surface.blit(text,(x,self.surface.size[1]/2-text.size[1]/2))
            for i in _k.getPressed().items():
                if i[1]:
                    if i[0] not in self.wclk:
                        if len(i[0]) == 1:
                            self.insert(i[0])
                        elif i[0] == 'backspace':
                            self.delete()
                        elif i[0] == 'return':
                            self.focus = False
                        elif i[0] == 'space':
                            self.insert(' ')
                        self.wclk.append(i[0])
                else:
                    if i[0] in self.wclk:
                        self.wclk.remove(i[0])
            self.tick += 1
            if self.tick >= 60:
                if self.text != '':
                    points = [[x+text.size[0],self.surface.size[1]/2-text.size[1]/2],
                              [x+text.size[0],self.surface.size[1]/2-text.size[1]/2+self.surface.size[1]-10]]
                    self.surface.draw.line(self.lineColor,points[0],points[1],3)
            if self.tick == 120:
                self.tick = 0
        else:
            self.surface.draw.rect(self.bg,_r(self.borderWidth,self.borderWidth,
                                self.surface.size[0]-self.borderWidth*2,
                                self.surface.size[1]-self.borderWidth*2))
            if self.text == '':
                text = self.font.render(self.hint,self.fontSize,self.hintColor)
            else:
                text = self.font.render(self.text,self.fontSize,self.fg)
            x = self.surface.size[0]/2-text.size[0]/2
            if text.size[0] >= self.surface.size[0]-20:
                x = self.surface.size[0]-text.size[0]-10
            self.surface.blit(text,(x,self.surface.size[1]/2-text.size[1]/2))

        if position != None:
            if self.surface.rect(position[0],
                                 position[1]).contains(_m.getPosition()[0],
                                                       _m.getPosition()[1]):
                if not self.wcl:
                    _m.setCursor(_pg.SYSTEM_CURSOR_HAND)
                else:
                    if not self.ws:
                        _m.setCursor(_pg.SYSTEM_CURSOR_ARROW)
                        self.ws = True
                if _m.isPressed('left'):
                    if not self.wcl:
                        self.focus=self.focus==0
                        self.wcl = True
                else:
                    self.wcl = False
                self.wsnr = False
            else:
                if not self.wsnr:
                    _m.setCursor(_pg.SYSTEM_CURSOR_ARROW)
                    self.wsnr = True
                if _m.isPressed('left'):
                    self.focus = False
    def insert(self,text):
        if _ct.WinDLL("User32.dll").GetKeyState(0x14):
            text = text.upper()
        if hex(getattr(_ct.windll.LoadLibrary("user32.dll"), "GetKeyboardLayout")(0))=='0x4190419':
            text = text.translate(dict(zip(map(ord,
            '''qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOPASDFGHJKLZXCVBNM'''),
            '''йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗФЫВАПРОЛДЯЧСМИТЬ''')))
        if _pg.key.get_pressed()[_pg.K_LSHIFT] or _pg.key.get_pressed()[_pg.K_RSHIFT]:
            text = text.translate(dict(zip(map(ord,
            u'''1234567890-=[]\;',./`'''),
            u'''!@#$%^&*()_+{}|:"<>?~''')))
        if text in self.blacklist:
            return
        if self.whitelist != None:
            if text not in self.whitelist:
                return
        if self.maxSymbols != None:
            if len(self.text) > self.maxSymbols:
                return
        self.text += text
    def delete(self,symbols=1):
        self.text = self.text[:0-symbols]
    def draw(self, win, pos):
        self._generate(pos)
        win.blit(self.surface,pos)
    def get(self):
        return self.text
class textarea(widget):
    def __init__(self,hint='',fontSize=30,
                 font=_df,width=None,bg=(70,70,70),
                 fg=(180,180,200),afg=(200,200,200),
                 abg=(50,50,50),hintColor=(100,100,100),
                 lineColor=(200,200,200),
                 borderColor=(50,50,50),
                 borderWidth=5,maxSymbols=None,
                 whitelist=None,blacklist=[]):
        super()._args(locals())
        self.text = ''
        self.focus = False
        self.tick = 0
        self.wcl = False
        self.startHint = self.hint
        self.ws = False
        if self.hint != '':
            hintSize = self.font.size(self.hint,self.fontSize)
        else:
            hintSize = (150,self.font.size('X',self.fontSize)[1])
        self.height = hintSize[1]+10
        if self.width == None:
            self.width = hintSize[0]+50
        self.surface = _s((self.width,self.height))
        self.wclk = []
        self.wsnr = False
    def _generate(self,position=None):
        self.surface.fill(self.borderColor)
        if self.focus:
            if self.text != '':
                self.height = self.font.size(self.text,self.fontSize)[1]+10
            else:
                self.height = self.font.size('X',self.fontSize)[1]+10
            self.surface = _s((self.width,self.height))
            self.surface.fill(self.borderColor)
            self.surface.draw.rect(self.abg,_r(self.borderWidth,self.borderWidth,
                                self.surface.size[0]-self.borderWidth*2,
                                self.surface.size[1]-self.borderWidth*2))
            if self.text == '':
                text = self.font.render(self.hint,self.fontSize,self.hintColor)
            else:
                text = self.font.render(self.text,self.fontSize,self.afg)
            try:
                last = self.text.split('\n')[-1]
            except:
                last = self.text
            x = 10
            if self.font.size(last,self.fontSize)[0] >= self.surface.size[0]-20:
                x = self.surface.size[0]-self.font.size(last,self.fontSize)[0]
            self.surface.blit(text,(x,self.surface.size[1]/2-text.size[1]/2))
            for i in _k.getPressed().items():
                if i[1]:
                    if i[0] not in self.wclk:
                        if len(i[0]) == 1:
                            self.insert(i[0])
                        elif i[0] == 'backspace':
                            self.delete()
                        elif i[0] == 'return':
                            if self.maxSymbols != None:
                                if len(self.text) > self.maxSymbols:
                                    continue
                            self.text += '\n'
                        elif i[0] == 'space':
                            self.insert(' ')
                        self.wclk.append(i[0])
                else:
                    if i[0] in self.wclk:
                        self.wclk.remove(i[0])
            self.tick += 1
            if self.tick >= 60:
                if self.text != '':
                    points = [[x+self.font.size(last,self.fontSize)[0],
                               self.surface.size[1]-(self.font.size('X',self.fontSize)[1])],
                              [x+self.font.size(last,self.fontSize)[0],
                               self.surface.size[1]/2-text.size[1]/2+self.surface.size[1]-10]]
                    self.surface.draw.line(self.lineColor,points[0],points[1],3)
            if self.tick == 120:
                self.tick = 0
        else:
            self.surface.draw.rect(self.bg,_r(self.borderWidth,self.borderWidth,
                                self.surface.size[0]-self.borderWidth*2,
                                self.surface.size[1]-self.borderWidth*2))
            if self.text == '':
                text = self.font.render(self.hint,self.fontSize,self.hintColor)
            else:
                text = self.font.render(self.text,self.fontSize,self.fg)
            try:
                last = self.text.split('\n')[-1]
            except:
                last = self.text
            x = self.surface.size[0]/2-text.size[0]/2
            if self.font.size(last,self.fontSize)[0] >= self.surface.size[0]-20:
                x = self.surface.size[0]-self.font.size(last,self.fontSize)[0]
            self.surface.blit(text,(x,self.surface.size[1]/2-text.size[1]/2))

        if position != None:
            if self.surface.rect(position[0],
                                 position[1]).contains(_m.getPosition()[0],
                                                       _m.getPosition()[1]):
                if not self.wcl:
                    _m.setCursor(_pg.SYSTEM_CURSOR_HAND)
                else:
                    if not self.ws:
                        _m.setCursor(_pg.SYSTEM_CURSOR_ARROW)
                        self.ws = True
                if _m.isPressed('left'):
                    if not self.wcl:
                        self.focus=self.focus==0
                        self.wcl = True
                else:
                    self.wcl = False
                self.wsnr = False
            else:
                if not self.wsnr:
                    _m.setCursor(_pg.SYSTEM_CURSOR_ARROW)
                    self.wsnr = True
                if _m.isPressed('left'):
                    self.focus = False
    def insert(self,text):
        if _ct.WinDLL("User32.dll").GetKeyState(0x14):
            text = text.upper()
        if _pg.key.get_pressed()[_pg.K_LSHIFT] or _pg.key.get_pressed()[_pg.K_RSHIFT]:
            text = text.translate(dict(zip(map(ord, '''1234567890-=[]\\;'''+"',./`"),
                                                    '''!@#$%^&*()_+{}|:"<>?~''')))
        if hex(getattr(_ct.windll.LoadLibrary("user32.dll"),
                       "GetKeyboardLayout")(0))=='0x4190419':
            text = text.translate(dict(zip(map(ord,
            '''qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'''),
            '''йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё''')))
        if text in self.blacklist:
            return
        if self.whitelist != None:
            if text not in self.whitelist:
                return
        if self.maxSymbols != None:
            if len(self.text) > self.maxSymbols:
                return
        self.text += text
    def delete(self,symbols=1):
        self.text = self.text[:0-symbols]
    def draw(self, win, pos):
        self._generate(pos)
        win.blit(self.surface,pos)
    def get(self):
        return self.text
class keySelect(entry):
    def __init__(self,keyBefore='',
                 fontSize=30,font=_df,
                 width=None,height=None,
                 bg=(70,70,70),fg=(180,180,200),
                 afg=(200,200,200),abg=(50,50,50),
                 hintColor=(100,100,100),
                 lineColor=(200,200,200),
                 borderColor=(50,50,50),
                 borderWidth=5,maxSymbols=None,
                 whitelist=None,blacklist=[]):
        super()._args(locals())
        self.hint = ''
        self.text = keyBefore
        self.focus = False
        self.tick = 0
        self.wcl = False
        self.startHint = self.hint
        self.ws = False
        if self.width == None or self.height == None:
            if self.hint != '':
                hintSize = self.font.size(self.hint,self.fontSize)
            else:
                hintSize = (150,self.font.size('X',self.fontSize)[1])
            if self.height == None:
                self.height = hintSize[1]+10
            if self.width == None:
                self.width = hintSize[0]+50
        self.surface = _s((self.width,self.height))
        self.wclk = []
        self.wsnr = False
    def _generate(self,position=None):
        self.surface.fill(self.borderColor)
        if self.focus:
            self.surface.draw.rect(self.abg,_r(self.borderWidth,self.borderWidth,
                                self.surface.size[0]-self.borderWidth*2,
                                self.surface.size[1]-self.borderWidth*2))
            if self.text == '':
                text = self.font.render(self.hint,self.fontSize,self.hintColor)
            else:
                text = self.font.render(self.text,self.fontSize,self.afg)
            x = self.surface.size[0]/2-text.size[0]/2
            if text.size[0] >= self.surface.size[0]-20:
                x = self.surface.size[0]-text.size[0]-10
            self.surface.blit(text,(x,self.surface.size[1]/2-text.size[1]/2))
            for i in _k.getPressed().items():
                if i[1] and self.focus:
                    if i[0] in self.blacklist:
                        continue
                    if self.whitelist != None:
                        if i[0] not in self.whitelist:
                            continue
                    if self.maxSymbols != None:
                        if len(self.text) > self.maxSymbols:
                            continue
                    self.text = i[0]
                    break
            self.tick += 1
            if self.tick >= 60:
                if self.text != '':
                    points = [[x+text.size[0],self.surface.size[1]/2-text.size[1]/2],
                              [x+text.size[0],self.surface.size[1]/2-text.size[1]/2+self.surface.size[1]-10]]
                    self.surface.draw.line(self.lineColor,points[0],points[1],3)
            if self.tick == 120:
                self.tick = 0
        else:
            self.surface.draw.rect(self.bg,_r(self.borderWidth,self.borderWidth,
                                self.surface.size[0]-self.borderWidth*2,
                                self.surface.size[1]-self.borderWidth*2))
            if self.text == '':
                text = self.font.render(self.hint,self.fontSize,self.hintColor)
            else:
                text = self.font.render(self.text,self.fontSize,self.fg)
            x = self.surface.size[0]/2-text.size[0]/2
            if text.size[0] >= self.surface.size[0]-20:
                x = self.surface.size[0]-text.size[0]-10
            self.surface.blit(text,(x,self.surface.size[1]/2-text.size[1]/2))

        if position != None:
            if self.surface.rect(position[0],
                                 position[1]).contains(_m.getPosition()[0],
                                                       _m.getPosition()[1]):
                if not self.wcl:
                    _m.setCursor(_pg.SYSTEM_CURSOR_HAND)
                else:
                    if not self.ws:
                        _m.setCursor(_pg.SYSTEM_CURSOR_ARROW)
                        self.ws = True
                if _m.isPressed('left'):
                    if not self.wcl:
                        self.focus=self.focus==0
                        self.wcl = True
                else:
                    self.wcl = False
                self.wsnr = False
            else:
                if not self.wsnr:
                    _m.setCursor(_pg.SYSTEM_CURSOR_ARROW)
                    self.wsnr = True
                if _m.isPressed('left'):
                    self.focus = False
    def draw(self, win, pos):
        self._generate(pos)
        win.blit(self.surface,pos)
    def get(self):
        return self.text
class image(widget):
    def __init__(self, path):
        self.surface = _l(path)
class loadingBar(widget):
    def __init__(self,width,
                 height=50,
                 length=100,
                 bg=(70,70,70),
                 loadedColor=(50,200,50),
                 borderColor=(50,50,50),
                 borderWidth=5):
        super()._args(locals())
        self.loaded = 0
    def step(self,count=1):
        self.loaded += 1
        if self.loaded > self.length:
            self.loaded = self.length
    def set(self, x):
        self.loaded = x
        if self.loaded > self.length:
            self.loaded = self.length
    def reset(self):
        self.loaded = 0
    def get(self):
        return self.loaded
    def draw(self, win, pos):
        self.surface = _s((self.width,self.height))
        self.surface.fill(self.borderColor)
        self.surface.draw.rect(self.bg,_r(5,5,
                            self.surface.size[0]-10,
                            self.surface.size[1]-10))
        self.surface.draw.rect(self.loadedColor,_r(self.borderWidth,self.borderWidth,
                (self.surface.size[0]/self.length*self.loaded)-self.borderWidth*2,
                                        self.surface.size[1]-self.borderWidth*2))
        win.blit(self.surface, pos)
class slider(widget):
    def __init__(self,width,
                 bg=(70,70,70),
                 fg=(200,200,200),
                 horizontal=True):
        super()._args(locals())
        self.s = False
        self.x = 12.5
        self._generate(None)
    def _generate(self, pos):
        if self.horizontal:
            self.surface = _s((self.width,50))
            self.surface.draw.line(self.bg,[12.5,25],[self.width-12.5,25],10)
            self.surface.draw.circle(self.bg,[12.5,26],5)
            self.surface.draw.circle(self.bg,[self.width-12.5,26],5)
            self.surface.draw.circle(self.fg,[self.x,25],12.5)
        else:
            self.surface = _s((50,self.width))
            self.surface.draw.line(self.bg,[25,12.5],[25,self.width-12.5],10)
            self.surface.draw.circle(self.bg,[26,12.5],5)
            self.surface.draw.circle(self.bg,[26,self.width-12.5],5)
            self.surface.draw.circle(self.fg,[25,self.x],12.5)
        if pos != None:
            if _m.isPressed('left'):
                if self.horizontal:
                    rect = _r(pos[0]+5,pos[1],
                              self.surface.size[0]-10,
                              self.surface.size[1])
                    if rect.contains(_m.getPosition()[0],
                                     _m.getPosition()[1]) or self.s:
                        self.x = _m.getPosition()[0]-pos[0]
                        if self.x < 12.5: self.x = 12.5
                        if self.x > self.width-12.5: self.x = self.width-12.5
                        self.s = True
                else:
                    rect = _r(pos[0],pos[1]+5,
                              self.surface.size[0],
                              self.surface.size[1]-10)
                    if rect.contains(_m.getPosition()[0],
                                     _m.getPosition()[1]) or self.s:
                        self.x = _m.getPosition()[1]-pos[1]
                        if self.x < 12.5: self.x = 12.5
                        if self.x > self.width-12.5: self.x = self.width-12.5
                        self.s = True
            else:
                self.s = False
    def get(self):
        return int(self.x/(self.width-10)*101)
    def set(self, x):
        self.x = x/101*(self.width-10)
    def draw(self, win, pos):
        self._generate(pos)
        win.blit(self.surface, pos)
class checkBox(widget):
    def __init__(self,width=50,bg=(180,180,180),
                 fg=(50,180,50),afg=(70,200,70),
                 abg=(120,120,120),borderColor=(220,220,220),
                 borderWidth=5):
        super()._args(locals())
        self.cl0 = False
        self.cl1 = False
        self.nc0 = True
        self.x = False
        self._generate()
    def set(self, x):
        self.x = x
    def get(self):
        return self.x
    def _generate(self, position=None):
        self.surface = _s((self.width,self.width))
        if position != None:
            contains = self.surface.rect(position[0], position[1]).contains(
                                    _m.getPosition()[0], _m.getPosition()[1])
            cacm = contains and _m.isPressed('left')
        else:
            contains = False
            cacm = False
        if contains and not self.cl0:
            _m.setCursor(_pg.SYSTEM_CURSOR_HAND)
            self.cl0 = True
            self.nc0 = True
        elif not contains:
            if self.nc0:
                _m.setCursor(_pg.SYSTEM_CURSOR_ARROW)
                self.nc0 = False
            self.cl0 = False
        if cacm and not self.cl1:
            self.x=self.x==0
            self.cl1 = True
        elif not cacm:
            self.cl1 = False
        self.surface.fill(self.borderColor)
        if cacm:
            self.surface.draw.rect(self.abg,_r(self.borderWidth,self.borderWidth,
                                self.surface.size[0]-self.borderWidth*2,
                                self.surface.size[1]-self.borderWidth*2))
            if self.x:
                self.surface.draw.line(self.afg,[self.borderWidth,self.width/2+self.borderWidth],
                                       [self.width/2,self.width-self.borderWidth],self.borderWidth)
                self.surface.draw.line(self.afg,[self.width/2,self.width-self.borderWidth],
                                       [self.width-self.borderWidth,self.borderWidth],self.borderWidth)
        else:
            self.surface.draw.rect(self.bg,_r(self.borderWidth,self.borderWidth,
                                self.surface.size[0]-self.borderWidth*2,
                                self.surface.size[1]-self.borderWidth*2))
            if self.x:
                self.surface.draw.line(self.fg,[self.borderWidth,self.width/2+self.borderWidth],
                                       [self.width/2,self.width-self.borderWidth],self.borderWidth)
                self.surface.draw.line(self.fg,[self.width/2,self.width-self.borderWidth],
                                       [self.width-self.borderWidth,self.borderWidth],self.borderWidth)
    def draw(self, win, pos):
        self._generate(pos)
        win.blit(self.surface,pos)
# class colorPicker(widget):
#     def __init__(self):
#         self._generate()
#     def _generate(self, position=None):
#         self.surface = _s((255,self.width))
#
#     def draw(self, win, pos):
#         self._generate(pos)
#         win.blit(self.surface,pos)
class tip(widget):
    def __init__(self,text,responceWidth,responceHeight,fontSize=15,font=_df,
                 borderColor=(180,180,50),borderWidth=2,bg=(255,255,128),
                 fg=(35,35,5),waitBeforeShowing=0,
                 tipPosRelativeCursor=(10,10)):
        super()._args(locals())
        self.tick = -1
        self.lcp = (0,0)
        self.tprc = self.tipPosRelativeCursor
        self._generate()
    def _generate(self, position=None):
        self.surface = _s((self.responceWidth,
                           self.responceHeight))
        if position != None:
            self.tick += 1
            if self.lcp != _m.getPosition():
                self.tick = 0
                self.lcp = _m.getPosition()
            if self.tick >= self.waitBeforeShowing:
                mp = _m.getPosition()
                mp = [mp[0]+self.tprc[0]-position[0],
                      mp[1]+self.tprc[1]-position[1]]
                rect = _r(mp[0],mp[1],
                self.font.size(self.text,self.fontSize)[0]+4,
                self.font.size(self.text,self.fontSize)[1]+6)
                if mp[0]<0 or mp[1]<0:return
                if mp[0]>self.responceWidth:return
                if mp[1]>self.responceHeight:return
                if mp[0]>self.responceWidth-rect.w:
                    mp[0]=self.responceWidth-rect.w
                if mp[1]>self.responceHeight-rect.h:
                    mp[1]=self.responceHeight-rect.h
                rect = _r(mp[0],mp[1],
                self.font.size(self.text,self.fontSize)[0]+4,
                self.font.size(self.text,self.fontSize)[1]+6)
                self.surface.draw.rect(self.bg,rect)
                self.surface.draw.rect(
                self.borderColor,rect,self.borderWidth)
                ts = self.font.render(
                self.text,self.fontSize,self.fg)
                self.surface.blit(ts,(mp[0]+2,mp[1]+3))
    def draw(self, win, pos):
        self._generate(pos)
        win.blit(self.surface,pos)

class base:
    def __init__(self, win, bg=(128,128,128)):
        self._widgets = {}
        self._bg = bg
        self._win = win
        self._page = 0
    def draw(self):
        self._win.fill(self._bg)
        for i in self._widgets[self._page]:
            if i[0].power:
                i[0].draw(self._win, i[1])
            if i[0].destroyed:
                self._widgets[self._page].remove(i)
    def put(self, widget, pos, page=0):
        if page not in self._widgets:
            self._widgets.update({page:[]})
        self._widgets[page].append([widget, pos])
    def selectPage(self, page):
        self._page = page
    def getPage(self):
        return self._page
    def getWidgets(self, page=0):
        return self._widgets[page]
    def setWidgetPos(self,index,pos,page=0):
        self._widgets[page][index] = [self._widgets[page][index][0], pos]
