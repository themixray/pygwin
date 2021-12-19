from pygwin._pg import pg as _pg
from pygwin.surface import surface as _surface
from PIL import Image as _im
import tempfile as _tf
import randstr as _rs
import pickle as _p
import bz2 as _bz2
import os as _os

def load(path):
    if path.endswith('.gif'):
        im = _im.open(path)
        with _tf.TemporaryDirectory() as td:
            surfs = []
            for i in range(im.n_frames):
                im.seek(i)
                p = _os.path.join(td,f'{i}.png')
                im.save(p)
                s = _pg.image.load(p)
                _os.remove(p)
                sg = _surface(s.get_size())
                sg.blit(s,(0,0))
                surfs.append(sg)
        return surfs
    else:
        im = _im.open(path.encode('utf8').decode('utf8'))
        image = _pg.image.fromstring(im.tobytes(),im.size,im.mode)
        surf = _surface(im.size)
        surf.blit(image,(0,0))
        return surf

def save(surface, dest):
    _pg.image.save_extended(surface._grp(), dest)

def toBytes(surface):
    return _bz2.compress(_p.dumps([_pg.image.tostring(surface._grp(),"RGBA"),list(surface.size)]))

def fromBytes(bytes):
    string = _p.loads(_bz2.decompress(bytes))
    surf = _pg.image.fromstring(string[0],tuple(string[1]),"RGBA")
    surface = _surface(tuple(string[1]))
    surface.blit(surf,(0,0))
    return surface
