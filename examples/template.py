import pygwin

win = pygwin.create('Title',(500,500))

run = True
while run:
    for event in pygwin.getEvents():
        if event.type == pygwin.QUIT:
            run = False

    win.update()
pygwin.close()
