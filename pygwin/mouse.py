from pygwin._pg import pg as _pg

def getPressed():
    orig = _pg.mouse.get_pressed(3)
    return {'left':orig[0],'middle':orig[1],'right':orig[2]}
def isPressed(x):
    return getPressed()[x]
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
