import pygame as pg
import time
pg.init()
def printtext(text,font,x,y,color=(255,255,255),shadow=0):
    screen = pg.display.get_surface()
    if shadow:
        image=font.render(text,True,(0,0,0))
        screen.blit(image,(x+shadow,y+shadow))
    image=font.render(text,True,color)
    screen.blit(image,(x,y))
    pg.display.update()
def draw_logo(ft=None):
    scr=pg.display.get_surface()
    wid,hei=scr.get_size()
    scr.fill((255,255,255))
    for i in range(hei//15):
        pg.draw.rect(scr,(0,0,0),(wid//11,hei//2-i,wid//5*4,i*2))
        #time.sleep(0.01)
        pg.display.update()
    time.sleep(0.03)
    printtext('Deep Cloud',pg.font.Font(ft,wid//5),wid//11+5,hei//2-hei//15)
    printtext('Loading...',pg.font.Font(ft,wid//10),wid//11+30,hei//2-hei//15+140,(110,100,120))