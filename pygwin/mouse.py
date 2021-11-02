from pygwin._pg import pg as _pg

def isPressed(x):
    return _pg.mouse.get_pressed()[x]
def getPressed():
    return _pg.mouse.get_pressed()
def setPosition(x):
    _pg.mouse.set_pos(x)
def getPosition():
    return _pg.mouse.get_pos()
def setVisible(x):
    _pg.mouse.set_visible(x)
def getVisible():
    return _pg.mouse.get_visible()
def getCursor():
    return _pg.mouse.get_cursor()
def setCursor(size, hotspot=None, xormasks=None, andmasks=None):
    if hotspot == None and xormasks == None and andmasks == None:
        _pg.mouse.set_system_cursor(size)
    else:
        _pg.mouse.set_cursor(size, hotspot, xormasks, andmasks)
