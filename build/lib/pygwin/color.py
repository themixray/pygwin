class color:
    def __init__(self,r,g=None,b=None,a=255):
        try:
            r,g,b = tuple(int(r[i:i+2],16)for i in(0,2,4))
        except:
            pass
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    def hex(self):
        return '%02x%02x%02x' % (self.r,self.g,self.b)
    def rgb(self):
        return (self.r,self.g,self.b,self.a)
    def inverse(self):
        return color(255-self.r,255-self.g,
                     255-self.b,255-self.a)
    def __getitem__(self,x):
        return [self.r,self.g,self.b,self.a][x]
    def __list__(self):
        return [self.r,self.g,self.b,self.a]
    def __tuple__(self):
        return self.rgb()
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return f'({",".join(str(i)for i in self.__list__())})'
