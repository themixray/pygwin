import pygwin
import random

win = pygwin.create(size=(500,500))

font = pygwin.defaultFont

run = True
while run:
    for event in pygwin.getEvents():
        if event.type == pygwin.QUIT:
            run = False
    win.fill((255,255,255))

    text = font.render(win.fps, 25, (0,0,0))
    text = pygwin.image.toString(text)
    win.blit(text,(0,0))
    text = pygwin.image.fromString(text)
    win.blit(text,(0,50))

    win.update(60)
pygwin.close()
