import pygame as pg
from core import *
import json
pg.init()
RES={}
json_config=None
config={}
RESIMG={}
RESITEM={}
RESMAC={}
ORE={}

def load_config():
    global json_config,config,ORE
    f=open('data/block.json')
    json_config=json.load(f)
    config.update(json_config[0]['texture'])
    ORE.update(json_config[0]['ore'])
    f.close()

def loadres(file):
    return pg.image.load('texture/'+file+'.png').convert_alpha()
def startload():
    global RES,RESIMG,RESMAC
    for rt in config['block']:
        name=rt.replace('.png','')
        RES.update({name:block(name,loadres(rt))})
    for rd in config['img']:
        name=rd.replace('.png','')
        RESIMG.update({name:loadres(rd)})
    for rdd in config['macine']:
        name=rdd.replace('.png','')
        RESMAC.update({name:macine(name,loadres(rdd))})
    for rddd in config['item']:
        name=rddd.replace('.png','')
        RESITEM.update({name:item(name,loadres(rddd))})
        