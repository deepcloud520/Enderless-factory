import pygame as pg
import local
import json
from gamelogger import *
pg.init()
RES={}
json_config=None
config={}
RESIMG={}
ORE={}
RESITEMS={}
VERSION='Omega 0.0.0 (Load Failed)'
MUSIC_ON=False

def load_config():
    global json_config,config,ORE
    f=open('data/gamedata.json',encoding='utf-8')
    json_config=json.load(f)
    config.update(json_config[0]['items'])
    ORE.update(json_config[0]['ore'])
    VERSION=json_config[1]['version']
    f.close()
    logger('basic config load complete.','info')
    return json_config
def loadres(file):
    return pg.image.load(file+'.png').convert_alpha()
'''
def getobject(obj,name):
    lt=dir(obj)
    return getattr(obj,name,None)
'''
def startload():
    global RESIMG,RESITEMS
    for itemname,value in config.items():
        texture=loadres(value['texture'])
        typegetting=vars(local)[value['type']]
        vardict={'name':itemname,'texture':texture}
        vardict.update(value['vars'])
        RESITEMS.update({itemname:typegetting(**vardict)})
    for imgname,path in json_config[0]['texture'].items():
        texture=loadres(path)
        RESIMG.update({imgname:texture})
    logger('texture load complete','info')
        
