from core import *
from pygame.locals import *
import pygame as pg
from gamelogger import logger
from configmanager import *
from local import *
import gameGUI as GUI
import sys,os,deepcloud
import saveworld as save

json_config=None
pg.init()
gamestat=0
target=None
def savenow():
    global g
    logger('world saving...','info')
    pkg=save.worldcase()
    pkg.dump(g,'player','mouse')
    f=open('save/'+target,mode='wb')
    f.write(pkg.picgame)
    f.close()
    logger('world save done.','info')
def intogame():
    global gamestat
    gamestat=1
def exitgame():
    logger('game exit.','info')
    sys.exit()
def nw():
    global gamestat
    gamestat=2
def loadgame():
    global g,gamestat
    if not target:return
    f=open('save/'+target,mode='rb')
    wc=save.worldcase()
    wc.picgame=f.read()
    f.close()
    g=wc.load().load(scr)
    gamestat=5
def cg():
    pass
def changetarget(sid):
    global target
    target=sid
def back():
    global gamestat
    gamestat=0
    fm.hidecont('2')
    fm.showcont('1')
if __name__=='__main__':
    logger('Welcome to enderless factory','info')
    
    scr=pg.display.set_mode(WINDOW._list())
    json_config=load_config()
    startload()
    save.init(config,resitems=RESITEMS,resimg=RESIMG,version=VERSION,jsonconfig=json_config)
    pg.display.set_caption('Enderless Factory '+json_config[1]['version'])
    # continue the GUI and welcome screen
    if not int(json_config[1]['debug']): 
        deepcloud.draw_logo()
    fm=GUI.framemanager()
    f=GUI.frame(point(0,0),WINDOW.x,WINDOW.y,scr,sid='1')
    f.addcont(GUI.button('newworld',point(270,300),intogame,170,40,(100,100,50),(255,255,255),scr))
    f.addcont(GUI.button('load',point(270,345),nw,170,40,(100,100,50),(255,255,255),scr))
    f.addcont(GUI.button('exit',point(270,390),exitgame,170,40,(100,100,50),(255,255,255),scr))
    f.addcont(GUI.label('Enderless Factory',point(160,90),scr,(200,200,200),(50,100,100),GUI.big_font))
    f.addcont(GUI.label(json_config[1]['version'],point(300,150),scr,(100,200,150),(50,100,100),GUI.nm_font))
    logger('GUI init complete.','info')
    fsave=GUI.frame(point(0,0),WINDOW.x,WINDOW.y,scr,sid='2')
    fsave.addcont(GUI.label('选择存档...',point(WINDOW.y//2,10),scr,(200,100,200),(50,100,100),GUI.middle_font))
    fsave.addcont(GUI.button('start!',WINDOW.copy()-point(100,40),loadgame,100,40,(100,100,50),(255,255,255),scr))
    fsave.addcont(GUI.button('back',WINDOW-point(WINDOW.x,40),back,100,40,(100,100,50),(255,255,255),scr))
    fm.addcont(f)
    fm.addcont(fsave)
    fm.hidecont('2')
    if int(json_config[1]['music']):
        logger('music loading.','info')
        channel=pg.mixer.find_channel(True)
        music=[]
        r.shuffle(json_config[1]['playlist'])
        for sound in json_config[1]['playlist']:
            music.append(pg.mixer.Sound('music/'+sound+'.ogg'))
            print('.',end='')
        logger('music load complete.','info')
        channel.set_endevent(USEREVENT)
        NOWPLAY=0
        channel.play(music[NOWPLAY])
    while True:
        for evt in pg.event.get():
            if evt.type==QUIT:exitgame()
            if evt.type==USEREVENT and int(json_config[1]['music']):
                NOWPLAY+=(1 if NOWPLAY<len(music)-1 else 0)
                channel.play(music[NOWPLAY])
        mps=pg.mouse.get_pos()
        keys=pg.key.get_pressed()
        scr.fill((0,0,0))
        fm.handle()
        fm.draw()
        pg.display.update()
        if gamestat==1:
            break
        if gamestat==2:
            pt=point(300,150)
            for file in os.listdir('save/'):
                fsave.addcont(GUI.button(file,pt,changetarget,170,40,(100,100,50),(255,255,255),scr,sid=file,hold_on=True))
                pt.y+=45
            fm.showcont('2')
            fm.hidecont('1')
            gamestat=3
        if gamestat==4 or gamestat==5:
            break
        if gamestat==3:
            pass
    logger('game start.','info')
    if gamestat==1:
        g=game(scr,'swwm',RESIMG['player'],RESIMG['mouse'],json_config)
        '''
        g.player.bag.append(['grass2',114514])
        g.player.bag.append(['itemcoal',114514])
        g.player.bag.append(['itemiron',114514])
        g.player.bag.append(['stone2',114514])
        '''
    while True:
        for evt in pg.event.get():
            if evt.type==QUIT:
                savenow()
                exitgame()
        mps=pg.mouse.get_pos()
        g.mousehandle(pg.mouse.get_pressed(),point(mps[0],mps[1]))
        keys=pg.key.get_pressed()
        if keys[K_UP]:g.move('up')
        elif keys[K_DOWN]:g.move('down')
        elif keys[K_RIGHT]:g.move('right')
        elif keys[K_LEFT]:g.move('left')
        elif list(keys)[48:48+MAXITEM+1].count(1)>0:
            g.change_select(list(keys)[48:48+MAXITEM+1].index(1)-1)
        elif keys[K_e]:
            g.opentable()
        scr.fill((0,0,0))
        g.draw()
        pg.display.update()
