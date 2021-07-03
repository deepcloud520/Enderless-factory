# ▒▒▒█████████████▒▒▒
# ▒▒███████████████▒▒
# ▒████████████████▒▒
# ▒███████▒████▒████▒
# ▒████▒██▒▒██▒▒▒███▒
# ████▒▒▒▒▒▒▒▒▒▒▒███▒
# ██▒█▒▒▒▒▒▒▒▒▒▒▒████
# ██▒▒▒▒██▒▒▒▒██▒████
# ███▒▒▒▒▒▒▒▒▒▒▒▒▒███
# ████▒▒▒▒▒██▒▒▒▒▒███
# ██████▒▒▒▒▒▒▒▒▒████
# ███████▒▒▒▒▒▒▒█████
# ▒█▒█████▒▒██████▒█▒
# ▒▒▒█▒▒▒█▒▒█▒▒▒▒▒▒▒▒
# ▒▒▒▒▒███████▒▒▒▒▒▒▒
# ▒▒▒██▓█████▓███▒▒▒▒
# ▒▒█▓█▓▓▓▓▓▓▓▓███▒▒▒
# ▒█▓██▒▒▒▒▒▒▒▒▒█▓█▒▒
# ▒█▓█▓▓▓▓▓▓▓▓▓▓█▓█▒▒
# ▒███▒▒▒▒▒▒▒▒▒▒███▒▒
# ▒█▒█▓▓▓▓▓▓▓▓▓▓█▒█▒▒
# ▒███▓▓▓▓▓▓▓▓▓▓███▒▒
# ▒▒▒█▓▓▓▓███▓▓▓█▒▒▒▒
# ▒▒▒█▓▓▓▓█▒█▓▓▓█▒▒▒▒
# ▒▒▒██████▒█████▒▒▒▒
# ▒▒▒▒▒████▒████▒▒▒▒▒
# ▒▒▒▒█████▒█████▒▒▒▒

#
# Stay your Determination!
#
import pickle as pk
import copy
# load:file->game
# dump:game->file
'''
def init(cg,resimg,resitems,version,jsonconfig):
    global config,RESIMG,RESITEMS,VERSION,json_config
    config=cg
    json_config=jsonconfig
    VERSION=version
    RESIMG=resimg
    RESITEMS=resitems
    '''
class saveable:
    # implement
    def copy(self):
        return copy.copy(self)
    def dump(self):
        pass
    def load(self):
        pass
class worldcase:
    def __init__(self):
        self.picgame=None
    def dump(self,g):
        '''
        chunks=dict()
        for rel_pt,c in g.chunks.items():
            bk=[]
            secbk=[]
            for block in c.blocks:
                bk.append(mapblock(block.name))
            for secblock in c.secblocks:
                if secblock.name in :
                    secbk.append(mapblock(secblock.name))
                elif secblock.name :
                    secbk.append(secblock.dump())
            chunks.update({rel_pt:mapchunk(point(*rel_pt),c.flag,bk,secbk)})
        # step 2
        for rel_pt,c in chunks.items():
            c.loadchunks(chunks)
        items=[]
        for pos,it in g.items:
            items.append((pos,it.name))
        mg=mapgame(g.player.name,texture,mouse,json_config,g.player.pt,items,chunks,g.player.bag)
        self.picgame=pk.dumps(mg)
        '''
        self.picgame=pk.dumps(g.dump())
    def load(self):
        return pk.loads(self.picgame)
'''
class mapgame:
    def __init__(self,name,texture,mouse,cg,pt,items,chunks,bag):
        self.name=name
        self.config=cg
        self.bs=None
        self.pt=pt
        self.texture=texture
        self.player=mapplayer(name,texture,bag,pt)
        self.chunks=chunks
        self.items=items
        self.mouse=mouse
    def load(self,bs):
        # use non-init mode to get game object
        g=core.game(bs,self.name,RESIMG[self.texture],RESIMG[self.mouse],self.config,self.pt,nonload=True)
        # first:dump items
        for pos,item in self.items:
            g.items.append((pos,RESITEMS[item].copy()))
        # second:dump chunk
        for rel_pt,c in self.chunks.items():
            g.chunks.update(c.load())
        # third: dump player
        g.player=self.player.load()
        return g
class mapchunk:
    def __init__(self,rel_pt,flag,blocks,secblocks):
        self.rel_pt=rel_pt
        self.flag=flag
        self.blocks=blocks
        self.secblocks=secblocks
        self.chunks=[]
    def loadchunks(self,chunks):
        # step 2 to dump
        self.chunks=chunks
    def load(self):
        # return the core-chunk
        ret=core.chunk(self.rel_pt,self.chunks,self.flag)
        bk=[]
        secbk=[]
        for it in self.blocks:
            bk.append(it.load())
        for secit in self.secblocks:
            secbk.append(secit.load())
        ret.blocks=bk
        ret.secblocks=secbk
        return {self.rel_pt._list():ret}
'''