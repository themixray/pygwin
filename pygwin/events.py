from pygwin._pg import pg as _pg

def getEvents():
    return _pg.event.get()
