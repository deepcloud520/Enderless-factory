import random as rd
import pygame as pg
import sys,time
import copy

from local import *
from configmanager import *
from pygame.locals import *
import gamelogger
import gameGUI as GUI
from saveworld import saveable
from main import get_game

pg.init()
pg.mixer.init()
WINDOW=point(800,800)
CHUNKRANGE=10
CHUNKWID=CHUNKRANGE*16
SHOWRADIUS=1
SPEED=4
BEED=114514
DEEPTH=1
SCREENWID=(SHOWRADIUS+1)*CHUNKWID
MAXITEM=8

r=rd.Random(BEED)
nm_font=pg.font.Font(None,20)


def printtext(text,font,pt,bs,color=(255,255,255),shadow=0):
    screen = bs
    if shadow:
        image=font.render(text,True,(0,0,0))
        screen.blit(image,(pt.x+shadow,pt.y+shadow))
    image=font.render(text,True,color)
    screen.blit(image,(pt.x,pt.y))

class chunk(saveable):
    def __init__(self,rel_pt,chunks,flag=r.choice(['grass','stone','stone'])):
        self.relpt=rel_pt
        self.blocks=[]
        self.secblocks=[]
        self.flag=''
        # chunks->near this chunk
        self.chunks=chunks
    def get_block(self,pt,target=None):
        return (self.blocks if not target else target)[pt.y*CHUNKRANGE+pt.x]
    def set_block(self,pt,tg,target=None):
        (self.blocks if not target else target)[pt.y*CHUNKRANGE+pt.x]=tg
    def dekblock(self,pt):
        self.set_block(pt,RESITEMS['empty'].copy(),self.secblocks)
    def putblock(self,pt,tg):
        if self.get_block(pt,self.secblocks).name=='empty':
            self.set_block(pt,tg,self.secblocks)
    def getnearblock(self,pt,target=None):
        lst=[]
        if not target:target=self.blocks
        for x in range(3):
            for y in range(3):
                p=point(x-1,y-1)
                if pt.x+x<=0:
                    c=self.chunks.get(self.relpt-point(1,0),0)
                    if c:b=c.get_block(point(CHUNKRANGE-1,pt.y),target)
                    else:continue
                elif pt.x+x>CHUNKRANGE:
                    c=self.chunks.get(self.relpt-point(-1,0),0)
                    if c:b=c.getblock(point(0,pt.y),target)
                    else:continue
                elif pt.y+y<=0:
                    c=self.chunks.get(self.relpt-point(0,1),0)
                    if c:b=c.getblock(point(pt.x,CHUNKRANGE-1),target)
                    else:continue
                elif pt.y+y>CHUNKRANGE:
                    c=self.chunks.get(self.relpt-point(0,-1),0)
                    if c:b=c.getblock(point(pt.x,0),target)
                    else:continue
                else:
                    b=self.get_block(pt+p,target)
                lst.append(b)
        return lst
    def getnear(self,pt,name,target=None):
        i=0
        for n in self.getnearblock(pt,target):
            if n.name==name:
                i+=1
        return i
    def grass_init(self):
        self.secblocks=[]
        for i in range(CHUNKRANGE**2):
            self.secblocks.append(RESITEMS['empty'])
    def crt_new(self):
        # level 1
        for i in range(CHUNKRANGE**2):
            if r.randint(0,5 if self.flag=='grass' else 2):
                self.blocks.append(RESITEMS['grass'].copy())
            else:
                self.blocks.append(RESITEMS['stone'].copy())
        # Level 2
        for i in range(CHUNKRANGE**2):
            rn=r.randint(0,5)
            if rn<(2 if self.flag=='grass' else 3):
                self.secblocks.append(RESITEMS['grass2'].copy())
            elif rn<=3:
                self.secblocks.append(RESITEMS['stone2'].copy())
            else:
                self.secblocks.append(RESITEMS['empty'].copy())
        # level 1
        for mk in range(DEEPTH):
            for x in range(CHUNKRANGE):
                for y in range(CHUNKRANGE):
                    '''
                    #old map gener
                    num=self.getnear(point(x,y),'grass')
                    if num>(4 if self.flag=='grass' else 5):self.set_block(point(x,y),RESITEMS['grass'].copy())
                    elif num<(3 if self.flag=='grass' else 4):self.set_block(point(x,y),RESITEMS['stone'].copy())
                    '''
                    for blocktype in ['grass','stone']:
                        num=self.getnear(point(x,y),blocktype)
                        if num>2:
                            self.set_block(point(x,y),RESITEMS[blocktype].copy())
                    # add ores
                    for o,pand in ORE.items():
                        if r.randint(0,pand)==0:
                            self.set_block(point(x,y),RESITEMS[o].copy())
                    for blocktype in ['grass2','stone2','empty']:
                        num=self.getnear(point(x,y),blocktype,target=self.secblocks)
                        if num>2:
                            self.set_block(point(x,y),RESITEMS[blocktype].copy(),target=self.secblocks) 
        '''         
        # level 2
        for mk in range(DEEPTH):
            for x in range(CHUNKRANGE):
                for y in range(CHUNKRANGE):
        '''
        self.chunks=[]
    def draw(self,player,bs,tick):
        deffpt=point(WINDOW.x/2-player.pt.x+self.relpt.x*CHUNKWID,WINDOW.y/2-player.pt.y+self.relpt.y*CHUNKWID)
        for x in range(CHUNKRANGE):
            for y in range(CHUNKRANGE):
                s1=self.get_block(point(x,y))
                s2=self.get_block(point(x,y),self.secblocks)
                if hasattr(s2,'updata'):
                    s2.updata(tick)
                s1.draw(bs,deffpt+point(x*16,y*16))
                s2.draw(bs,deffpt+point(x*16,y*16))
    def dump(self):
        self.chunks=[]
        # begin to convert blocks
        tempbks=[]
        tempsecbks=[]
        for bk in self.blocks:
            tempbks.append(bk.dump())
        for secbk in self.secblocks:
            tempsecbks.append(secbk.dump())
        self.blocks=tempbks
        self.secblocks=tempsecbks
        return self
    def load(self):
        bk=[]
        secbk=[]
        for it in self.blocks:
            it.load()
            bk.append(it)
        for secit in self.secblocks:
            secit.load()
            secbk.append(secit)
        # load to chunk
        self.blocks=bk
        self.secblocks=secbk
class player(saveable):
    def __init__(self,name,texture,pt=point(0,0)):
        self.name=name
        self.texture=texture
        self.pt=pt
        self.lastpt=pt
        self.bag=[]
        self.nowselect=0
    def draw(self,bs):
        bs.blit(self.texture,(WINDOW.x/2,WINDOW.y/2))
    def move(self,way):
        ''' move(str,list(nowchunk,nowpoint)) '''
        tp=self.pt.copy()
        if way=='up':self.pt.y-=SPEED
        elif way=='down':self.pt.y+=SPEED
        elif way=='right':self.pt.x+=SPEED
        elif way=='left':self.pt.x-=SPEED
        self.lastpt=tp
    def check(self,way,now):
        floor=now[0].get_block(now[1],now[0].secblocks)
        left=now[2].get_block(now[3],now[2].secblocks)
        if floor.name!='empty'and left.name!='empty':
            self.pt=self.lastpt
    def additem(self,item,num=1):
        if item.name!='empty':
            i=0
            for it,nu in self.bag:
                if it==item.name:
                    self.bag[i][1]+=num
                    break
                i+=1
            else:
                if len(self.bag)<12:
                    self.bag.append([item.name,num])
    def getitem(self):
        if self.nowselect<len(self.bag):
            name,num=self.bag[self.nowselect]
        else:
            return
        ret=None
        if name in RESITEMS:
            ret=RESITEMS[name].copy()
            if self.bag[self.nowselect][1]>1:
                self.bag[self.nowselect][1]-=1
            else:
                self.bag.pop(self.nowselect)
            return ret
        else:
            # error
            pass
    def change_select(self,num):
        # input 0-MAXITEM-1
        if num<MAXITEM:
            self.nowselect=num
    # save
    def dump(self):
        self.texture=None
        return self
    def load(self):
        self.texture=getresour('player')
class crafttable(GUI.frame):
    class inlinelabel(GUI.label):
        def __init__(self,table,text,pt,scr,ftcolor,bgcolor=(255,255,255),ft=GUI.nm_font,sid=''):
            super().__init__(text,pt,scr,ftcolor,bgcolor,ft,sid)
            self.t=table
        def handle(self,mx,my,evt):
            if evt[0]:
                self.t.setfocus(self.sid)
                self.t.crafting(self.sid)
    def __init__(self,craftconfig,gameobject,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.craftconfig=craftconfig
        self.game=gameobject
        self.tatget=''
        pt=point(5,50)
        self.addcont(GUI.label(self,'合成...',point(2,2),self.scr,(150,150,120),(50,100,100),ft=GUI.middle_font,sid='title'))
        self.craftingtable=dict()
        for it,value in self.craftconfig.items():
            need=it+' '+','.join(['%s:%s' %(item,num) for item,num in value.items()])
            self.addcont(crafttable.inlinelabel(self,need,pt,self.scr,(150,150,80),(50,100,100),sid=it))
            self.craftingtable.update({it:[(item,num) for item,num in value.items()]})
            pt.y+=15
    def handle(self):
        super().handle()
    def setfocus(self,sid):
        self.target=sid
    def draw(self):
        super().draw()
    def crafting(self,sid):
        targetitem=sid
        value=self.craftingtable[targetitem]
        
        
class game(saveable):
    def __init__(self,bs,name,pt=point(0,0),nonload=False):
        self.player=player(name,getresour('player'),pt)
        self.chunks=dict()
        self.bs=bs
        if not nonload:
            self.newchunk(point(0,0))
            self.chunks[(0,0)].grass_init()
        self.items=[]
        # mouse vars
        self.mpos=point(0,0)
        self.mouse=getresour('mouse')
        # board
        self.board=pg.Surface((100,180))
        self.board.fill((50,60,80))
        # config
        self.config=getjsonconfig()
        self.guimanager=GUI.framemanager()
        # table
        self.table=crafttable(self.config[0]['crafttable'],gameobject=self,point(WINDOW.x//2-150,WINDOW.y//2-100),300,200,self.bs,sid='craft')
    def newitem(self,pt,item):
        self.items.append((pt,item))
    def removeitem(self,item):
        for pt,i in self.items:
            if i==item:
                self.items.remove((pt,i))
                return
    def newchunk(self,relpt,nearck=None):
        if nearck and nearck.flag=='grass':
            t=2
        else:
            t=1
        flag='grass' if r.randint(0,t)==0 else 'stone'
        c=chunk(relpt,self.chunks,flag)
        c.crt_new()
        self.chunks.update({relpt._list():c})
    def _getckpoint(self,pt,ckpt):
        # get pt in ckpt (usually use it in chunk's func)
        k=pt-ckpt*CHUNKWID
        x=k.x
        y=k.y
        if x<0:x=CHUNKWID-abs(x)
        if y<0:y=CHUNKWID-abs(y)
        return point(x//16,y//16)
    def getchunkpoint(self,pt):
        # get point of player in chunk
        return self._getckpoint(self.player.pt,pt)
    def getpoint(self,pot):
        # get pos form screen-pos to chunk-pos
        return point(pot.x//CHUNKWID,pot.y//CHUNKWID)
    def getplayernow(self):
        return self.getpoint(self.player.pt)
    def getchunk(self,relpt):
        # getchunk->get chunk in relpt
        c=self.chunks.get(relpt._list(),0)
        if c:
            return c
    def getblockpoint(self,pot):
        return point(pot.x//16,pot.y//16)
    def move(self,strs):
        pt=self.getplayernow()
        pt2=self.getpoint(pt*CHUNKWID+point(16,16))
        self.player.check(strs,[self.getchunk(pt),self.getchunkpoint(pt),self.getchunk(pt2),self.getchunkpoint(pt2)])
        self.player.move(strs)
    def drawmouse(self):
        self.bs.blit(self.mouse,(self.mpos)._list())
    def opentable(self):
        if self.guimanager.isin('craft'):
            # close the table
            self.guimanager.delcont('craft')
        else:
            self.guimanager.addcont(self.table,mux=True)
    def getblock(self,pos,layer=0):
        # layer:0=chunk.blocks 1=self.secblocks
        c=self.getchunk(self.getpoint(tp))
        if not c:
            return None
        pot=self._getckpoint(tp,c.relpt)
        return c.get_block(pot,target=c.blocks if layer==0 else c.secblocks)
    def setblock(self,pos,block,layer=0):
        # layer:0=chunk.blocks 1=self.secblocks
        c=self.getchunk(self.getpoint(tp))
        if not c:
            return None
        pot=self._getckpoint(tp,c.relpt)
        return c.set_block(pot,block,target=c.blocks if layer==0 else c.secblocks)
    def draw(self):
        # draw blocks
        i=0
        tx,ty=self.getplayernow()._list()
        addlst=[]
        for c in self.chunks.values():
            if c.relpt.x-SHOWRADIUS>tx or c.relpt.x+SHOWRADIUS<tx or c.relpt.y-SHOWRADIUS>ty or c.relpt.y+SHOWRADIUS<ty:
                continue
            i+=1
            # draw chunk
            tick=pg.time.get_ticks()
            c.draw(self.player,self.bs,tick)
            for x in range(3):
                for y in range(3):
                    if x==1 and y==1:continue
                    tp=c.relpt+point(x-1,y-1)
                    ck=self.getchunk(tp)
                    if not ck:addlst.append(tp)
        for v in addlst:
            self.newchunk(v,c)
        # check items
        rm=[]
        for pt,it in self.items:
            temp=self.getblockpoint(pt)
            pl=self.getblockpoint(self.player.pt)
            if temp.x==pl.x and temp.y==pl.y:
                rm.append(it)
                self.player.additem(it)
        for r in rm:
            self.removeitem(r)
        # draw items
        deffpt=point(WINDOW.x//2-self.player.pt.x,WINDOW.y//2-self.player.pt.y)
        for pt,it in self.items:
            # 8 -> item surface size
            if pt.x<self.player.pt.x-SCREENWID-8 or pt.x>self.player.pt.x+SCREENWID or pt.y<self.player.pt.y-SCREENWID-8 or pt.y>self.player.pt.y+SCREENWID:
                continue
            it.smdraw(self.bs,deffpt+pt)
        # debug text
        printtext('LOADCHUNK:'+str(i)+' '+str(self.player.pt)+
                  ' ALLCHUNKS:'+str(len(self.chunks)) +
                  ' chunkpos:' + str(self.getplayernow()) +
                  ' player_chunk:'+str(self.getchunkpoint(self.getplayernow())) +
                  ' mouse_pos:'+str(self.mpos) +
                  ' chunktype:'+self.chunks[self.getplayernow()._list()].flag
                  ,nm_font,point(1,1),self.bs)
        printtext(self.config[1]['version'],nm_font,point(1,15),self.bs,(50,80,150))
        # draw player
        self.player.draw(self.bs)
        self.drawmouse()
        # draw board
        self.bs.blit(self.board,(WINDOW.x-100,WINDOW.y-180))
        p=point(WINDOW.x-90,WINDOW.y-170)
        i=1
        for item,num in self.player.bag:
            dtemp=RESITEMS[item]
            if self.player.nowselect==i-1:
                # draw select
                pg.draw.rect(self.bs,(200,200,200),pg.Rect(p.x-2,p.y-2,88,16),2)
            dtemp.smdraw(self.bs,p)
            printtext(str(i),nm_font,point(p.x-10,p.y),self.bs,(100,100,100))
            printtext(str(num),nm_font,point(p.x+20,p.y),self.bs)
            p.y+=14
            i+=1
        #draw GUI
        self.guimanager.handle()
        self.guimanager.draw()
    def mousehandle(self,button,mpos):
        self.mpos=point(mpos.x//16*16,mpos.y//16*16)-point(self.player.pt.x%16,self.player.pt.y%16)
        if button[0]:
            # left click->delete block
            # tp-> abs block-pos
            tp=self.mpos-point(WINDOW.x//2,WINDOW.y//2)+self.player.pt
            c=self.getchunk(self.getpoint(tp))
            if not c:
                return False
            pot=self._getckpoint(tp,c.relpt)
            if c.get_block(pot,c.secblocks).name=='empty':
                return
            self.newitem(tp+point(r.randint(-2,2),r.randint(-2,2)),c.get_block(pot,target=c.secblocks))
            c.dekblock(pot)
            # new item
        elif button[2]:
            # right button
            tp=self.mpos-point(WINDOW.x//2,WINDOW.y//2)+self.player.pt
            c=self.getchunk(self.getpoint(tp))
            if not c:
                return False
            pot=self._getckpoint(tp,c.relpt)
            
            if c.get_block(pot,c.secblocks).name=='empty':
                i=self.player.getitem()
                if i:c.putblock(pot,i)
        else:pass
    def change_select(self,num):
        return self.player.change_select(num)
    # save
    def dump(self):
        # init 
        tempitems=[]
        tempchunks={}
        
        for pos,it in self.items:
            # change into pos,name
            tempitems.append((pos,it.name))
        for relpt,c in self.chunks.items():
            tempchunks.update({relpt:c.dump()})
        self.items=tempitems
        self.chunks=tempchunks
        self.table=None
        self.board=None
        self.mouse=None
        self.bs=None
        self.player.dump()
        return self
    def load(self):
        
        tempitems=[]
        tempchunks={}
        for pos,item in self.items:
            tempitems.append((pos,getitem(item)))
        # second:dump chunk
        for rel_pt,c in self.chunks.items():
            c.load()
            tempchunks.update({rel_pt:c})
        self.__init__(pg.display.get_surface(),self.player.name,nonload=True)
        self.items=tempitems
        self.chunks=tempchunks
        # third: dump player
        self.player.load()
