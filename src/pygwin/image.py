from pygwin._pg import pg as _pg
from pygwin.surface import surface as _surface
from PIL import Image as _im
import pickle as _p
import bz2 as _bz2

def load(path):
    if path.endswith('.gif'):
        im = _im.open(path)
        surfs = []
        for i in range(im.n_frames):
            im.seek(i)
            image = _pg.image.fromstring(im.tobytes(),im.size,im.mode)
            surf = _surface(image.get_size())
            surf._surface_orig = image
            surfs.append(surf)
        return surfs
    else:
        im = _im.open(path.encode('utf8').decode('utf8'))
        image = _pg.image.fromstring(im.tobytes(),im.size,im.mode)
        surf = _surface(im.size)
        surf.blit(image,(0,0))
        return surf

def save(surface, dest):
    if type(surface) == _surface:
        orig = surface._surface_orig
    else:
        orig = surface._orig
    _pg.image.save_extended(orig, dest)

def toBytes(surface):
    try:
        orig = surface._surface_orig
    except:
        orig = surface._orig
    return _bz2.compress(_p.dumps([_pg.image.tostring(orig,"RGBA"),list(surface.size)]))

def fromBytes(bytes):
    string = _p.loads(_bz2.decompress(bytes))
    surf = _pg.image.fromstring(string[0],tuple(string[1]),"RGBA")
    surface = _surface(tuple(string[1]))
    surface.blit(surf,(0,0))
    return surface
