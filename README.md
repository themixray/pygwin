# PyGWin
A library for creating Python applications.

[Documentation](https://github.com/themixray/pygwin/wiki)
***
## Quick Start
A simple game.
```python
import pygwin

win = pygwin.create('A Simple Game', (500,500))

x = 250
y = 250

run = True
while run:
    for event in pygwin.getEvents():
        if event.type == pygwin.QUIT:
            run = False
    win.fill((255,255,255))

    win.blit(win.fps,(0,0))
    win.draw.rect((0,0,0),pygwin.rect(x-10,y-10,20,20))

    if pygwin.keyboard.isPressed('w'):
        y -= 5
    if pygwin.keyboard.isPressed('s'):
        y += 5
    if pygwin.keyboard.isPressed('d'):
        x += 5
    if pygwin.keyboard.isPressed('a'):
        x -= 5

    if x <= -10:
        x = 510
    if y <= -10:
        y = 510
    if x > 510:
        x = -10
    if y > 510:
        y = -10

    win.update(60)
pygwin.close()
```
