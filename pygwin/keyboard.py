from pygwin._pg import pg as _pg

def getPressed():
    fkeys = {}
    keys = _pg.key.get_pressed()
    for i in range(len(keys)):
        fkeys.update({_pg.key.name(i):keys[i]})
    return fkeys
def isPressed(key):
    return getPressed()[key]
