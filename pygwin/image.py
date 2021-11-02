from pygwin._pg import pg as _pg
from pygwin.surface import surface as _surface
from PIL import Image as _image
import pickle as _p

def load(path):
    if path.endswith('.gif'):
        im = Image.open(path)
        surfs = []
        for i in range(im.n_frames):
            im.seek(i)
            image = _pg.image.fromstring(im.tobytes(),im.size,im.mode)
            surf = _surface(image.get_size())
            surf._surface_orig = image
            surfs.append(surf)
        return surfs
    else:
        image = _pg.image.load(path)
        surf = _surface(image.get_size())
        surf._surface_orig = image
        return surf

def save(surface, dest):
    if type(surface) == _surface:
        orig = surface._surface_orig
    else:
        orig = surface._orig
    _pg.image.save_extended(orig, dest)

def toString(surface):
    if type(surface) == _surface:
        orig = surface._surface_orig
    else:
        orig = surface._orig
    return _p.dumps([_pg.image.tostring(orig,"RGBA"),list(surface.size)],0)

def fromString(string):
    string = _p.loads(string, encoding='latin1')
    surf = _pg.image.fromstring(string[0],tuple(string[1]),"RGBA")
    surface = _surface(tuple(string[1]))
    surface._surface_orig = surf
    return surface
