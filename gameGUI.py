import pygame as pg
from pygame.locals import *
from local import *

pg.init()
nm_font=pg.font.Font('font/Liberation Mono.ttf',13)
big_font=pg.font.Font('font/Liberation Mono.ttf',40)
middle_font=pg.font.Font('font/MicrosoftYaqiHeiLight-2.ttf',24)
def printtext(text,font,pt,bs,color=(255,255,255),shadow=0):
    screen = bs
    if shadow:
        image=font.render(text,True,(0,0,0))
        screen.blit(image,(pt.x+shadow,pt.y+shadow))
    image=font.render(text,True,color)
    screen.blit(image,(pt.x,pt.y))
class cont:
    def __init(self):
        pass
    def draw(self,bs):
        pass
    def handle(self):
        pass
class button(cont):
    def __init__(self,text,pt,fun,weight,height,color,fontcolor,scr,hold_on=False,font=nm_font,sid=''):
        self.pt=pt
        self.h=height
        self.w=weight
        self.scr=scr
        self.sid=sid
        # init const button surface
        self.surface=pg.Surface((weight,height))
        self.surface.fill(color)
        printtext(text,nm_font,point(weight//len(text)-4,height//2-6),self.surface,fontcolor)
        self.press=pg.Surface((weight,height))
        self.press.fill(fontcolor)
        printtext(text,nm_font,point(weight//len(text)-4,height//2-6),self.press,color)
        # basic var
        self.holdon=hold_on
        self.keyflag=False
        self.fun=fun
    def draw(self):
        if not self.keyflag:
            self.scr.blit(self.surface,self.pt._list())
        else:
            self.scr.blit(self.press,self.pt._list())
    def handle(self,mx,my,evt):
        if evt[0]:
            if not self.keyflag:
                if mx<self.pt.x or my<self.pt.y or mx>self.pt.x+self.w or my>self.pt.y+self.h:
                    return False
                self.keyflag=True if self.holdon else False
                if self.sid:self.fun(self.sid)
                else:self.fun()
        if evt[2]:
            self.keyflag=False
class label(cont):
    def __init__(self,text,pt,scr,ftcolor,bgcolor=(255,255,255),ft=nm_font,sid=''):
        self.pt=pt
        self.scr=scr
        self.sid=sid
        image=ft.render(text,True,ftcolor)
        self.surface=pg.Surface(image.get_size())
        self.surface.fill(bgcolor)
        self.surface.blit(image,(0,0))
    def draw(self):
        self.scr.blit(self.surface,self.pt._list())
    def handle(self,*args):
        pass
class frame(cont):
    def __init__(self,pt,weight,height,scr,bgcolor=(50,100,100),sid=''):
        self.pt=pt
        self.scr=scr
        # sid -> frame id
        self.sid=sid
        self.contlst=[]
        self.w=weight
        self.h=height
        self.surface=pg.Surface((weight,height))
        self.surface.fill(bgcolor)
    def draw(self):
        self.scr.blit(self.surface,self.pt._list())
        for c in self.contlst:
            c.draw()
    def addcont(self,lastcont):
        lastcont.pt+=self.pt
        self.contlst.append(lastcont)
    def handle(self):
        if pg.mouse.get_pressed()[0]==1:
            mx,my=pg.mouse.get_pos()
            if mx<self.pt.x or my<self.pt.y or mx>self.pt.x+self.w or my>self.pt.y+self.h:
                return False
            # get local x,y
            mx-=self.pt.x
            my-=self.pt.y
            for c in self.contlst:
                c.handle(mx,my,pg.mouse.get_pressed())
class framemanager(frame):
    def __init__(self):
        self.mxlst=[]
        self.contlst=[]
        self.hide=[]
    def draw(self):
        for c in self.contlst:
            if c.sid not in self.hide:c.draw()
    def addcont(self,lastcont,mux=False):
        self.contlst.append(lastcont)
        if mux:
            # mux -> don't open frame again
            self.mxlst.append(lastcont.sid)
    def handle(self):
        for c in self.contlst:
            if c.sid not in self.hide:c.handle()
    def delcont(self,sid):
        for c in self.contlst:
            if c.sid==sid:
                self.contlst.remove(c)
                self.mxlst.remove(c.sid)
                return
    def isin(self,sid):
        return sid in self.mxlst
    def hidecont(self,sid):
        self.hide.append(sid)
    def showcont(self,sid):
        self.hide.remove(sid)
# Dont use dialog!!!
class dialog(frame):
    def __init__(self,title,pt,weight,height,scr,bgcolor=(255,180,180),titcolor=(100,100,255),ftcolor=(0,0,0)):
        self.pt=pt
        self.scr=scr
        self.contlst=[]
        self.w=weight
        self.h=height
        self.surface=pg.Surface((weight,height))
        self.surface.fill(bgcolor)
        pg.draw.rect(self.surface,titcolor,(0,0,weight,25),0)
        printtext(title,nm_font,weight//5,10,self.surface,ftcolor)
    def draw(self):
        self.scr.blit(self.surface,self.pt)
        for c in self.contlst:
            c.draw()
    def addcont(self,lastcont):
        lastcont.pt.x+=self.pt.x
        lastcont.pt.y+=self.pt.y
        self.contlst.append(lastcont)
    def handle(self):
        for evt in pg.event.get():
            if evt.type==MOUSEBUTTONDOWN or evt.type==MOUSEBUTTONUP:
                mx,my=evt.pt 
                if mx<self.pt.x or my<self.pt.y or mx>self.pt.x+self.w or my>self.pt.y+self.h:
                    return False
                mx-=self.pt.x
                my-=self.pt.y
                for c in self.contlst:
                     c.handle(mx,my,evt)
                
