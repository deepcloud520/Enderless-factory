import pygame as pg
from local import *
import json
from gamelogger import *
pg.init()
RES={}
json_config=None
config={}
RESIMG={}
RESITEM={}
RESMAC={}
ORE={}
RESITEMS={}
VERSION='Omega 0.0.0 (Load Failed)'
MUSIC_ON=False

def load_config():
    global json_config,config,ORE
    f=open('data/gamedata.json')
    json_config=json.load(f)
    config.update(json_config[0]['texture'])
    ORE.update(json_config[0]['ore'])
    VERSION=json_config[1]['version']
    f.close()
    config.update({'items':config['block']+config['item']})
    logger('basic config load complete.','info')
    return json_config
def loadres(file):
    return pg.image.load('texture/'+file+'.png').convert_alpha()
def startload():
    global RES,RESIMG,RESMAC,RESITEMS
    for rt in config['block']:
        name=rt.replace('.png','')
        RES.update({name:block(name,loadres(rt))})
    for rd in config['img']:
        name=rd.replace('.png','')
        RESIMG.update({name:loadres(rd)})
    for rdd in config['machine']:
        name=rdd.replace('.png','')
        RESMAC.update({name:machine(name,loadres(rdd))})
    for rddd in config['item']:
        name=rddd.replace('.png','')
        RESITEM.update({name:item(name,loadres(rddd))})
    RESITEMS.update(RESITEM)
    RESITEMS.update(RES)
    logger('texture load complete','info')
        