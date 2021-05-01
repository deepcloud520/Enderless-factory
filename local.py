import pygame as pg
import copy
import core
pg.init()

# Planktolovania

class point:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
    def _list(self):
        return (self.x,self.y)
    def copy(self):
        return point(self.x,self.y)
    def __add__(self,obj):
        return point(self.x+obj.x,self.y+obj.y)
    def __mul__(self,obj):
        # only mul int
        return point(self.x*obj,self.y*obj)
    def __sub__(self,obj):
        return point(self.x-obj.x,self.y-obj.y)
    def __div__(self,obj):
        return point(self.x/obj,self.y/obj)
    def __str__(self):
        return '{x:%s,y:%s}' %(self.x,self.y)
class item:
    def __init__(self,name,texture=None):
        self.texture=texture
        self.name=name
        self.sltexture=pg.transform.smoothscale(texture,(8,8)) if self.texture else None
    def smdraw(self,bs,pt):
        if self.sltexture:bs.blit(self.sltexture,pt._list())
    def copy(self):
        return copy.copy(self)
class block(item):
    def draw(self,bs,pt):
        if self.texture:bs.blit(self.texture,pt._list())
    def init(self,pt):
        self.pt=pt
class machine(block):
    def __init__(self,name,texture=None):
        super().__init__(name,texture)
        self.name=name
        self.inp=[]
        self.out=[]
        self.texture=texture
        self.dow=None
        self.near=[]
        self.ct=0
        self.down=''
    def putdown_init(self):
        pass
    def update(self):
        pass
    def iteminput(self,item):
        pass
    def itemoutput(self,item):
        pass
class oregen(machine):
    def __init__(self,name,cfg,texture=None):
        super().__init__(self,name,ctg,texture)
    def init(self,pt,game):
        super().init(pt)
        self.g=game
    def updata(self):
        if len(self.out)>0:
            for ck in g.getnear(self.point()):
                if 'output' in self.cfg:
                    ck.iteminput(self.out.pop())
                    break
        self.ct+=1
        if self.ct==10:
            self.ct=0
    def iteminput(self,item):
        self.inp.append(item)
    def itemoutput(self):
        return self.out.pop() if len(self.out)>0 else None
