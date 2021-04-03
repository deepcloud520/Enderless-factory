from core import *
from pygame.locals import *
import pygame as pg
from gamelogger import logger
from configmanager import *
from local import *
import gameGUI as GUI
import sys,os,deepcloud

json_config=None
pg.init()
gamestat=0
def intogame():
    global gamestat
    gamestat=1
def exitgame():
    logger('game exit.','info')
    sys.exit()
if __name__=='__main__':
    logger('Welcome to enderless factory','info')
    
    scr=pg.display.set_mode(WINDOW._list())
    json_config=load_config()
    startload()
    pg.display.set_caption('Enderless Factory '+json_config[1]['version'])
    # continue the GUI and welcome screen
    if not int(json_config[1]['debug']): 
        deepcloud.draw_logo()
        f=GUI.frame(point(0,0),WINDOW.x,WINDOW.y,scr)
        f.addcont(GUI.button('start',point(270,300),intogame,170,40,(100,100,50),(255,255,255),scr))
        f.addcont(GUI.button('exit',point(270,345),exitgame,170,40,(100,100,50),(255,255,255),scr))
        f.addcont(GUI.label('Enderless Factory',point(160,90),scr,(200,200,200),(50,100,100),GUI.big_font))
        f.addcont(GUI.label(json_config[1]['version'],point(300,150),scr,(100,200,150),(50,100,100),GUI.nm_font))
        logger('GUI init complete.','info')
        if int(json_config[1]['music']):
            logger('music loading.','info')
            channel=pg.mixer.find_channel(True)
            sound=pg.mixer.Sound('music/Blue.ogg')
            channel.play(sound)
            logger('music load complete.','info')
        while True:
            for evt in pg.event.get():
                if evt.type==QUIT:exitgame()
            mps=pg.mouse.get_pos()
            keys=pg.key.get_pressed()
            scr.fill((0,0,0))
            f.handle()
            f.draw()
            pg.display.update()
            if gamestat==1:
                break
    logger('game start.','info')
    g=game(scr,'swwm',RESIMG['player'],RESIMG['mouse'],json_config)
    g.player.bag.append(['grass2',114514])
    for file in os.listdir('save/'):
        pass
    
    while True:
        for evt in pg.event.get():
            if evt.type==QUIT:exitgame()
        mps=pg.mouse.get_pos()
        g.mousehandle(pg.mouse.get_pressed(),point(mps[0],mps[1]))
        keys=pg.key.get_pressed()
        if keys[K_UP]:g.move('up')
        elif keys[K_DOWN]:g.move('down')
        elif keys[K_RIGHT]:g.move('right')
        elif keys[K_LEFT]:g.move('left')
        elif list(keys)[48:48+MAXITEM+1].count(1)>0:
            g.change_select(list(keys)[48:48+MAXITEM+1].index(1)-1)
        scr.fill((0,0,0))
        g.draw()
        pg.display.update()
