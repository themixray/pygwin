# PyGWin
A library for creating Python applications.

[Documentation](https://github.com/themixray/pygwin/wiki)
***
## Quick Start
A simple game.
```python
import pygwin
import random

win = pygwin.create('A Simple Game', (500,500))

player = [250,250]
apple = pygwin.rect(random.randint(0,490),
                    random.randint(0,490),20,20)
count = 0

run = True
while run:
    for event in pygwin.getEvents():
        if event.type == pygwin.QUIT:
            run = False
    win.fill((255,255,255))

    playerRect = pygwin.rect(player[0]-10,player[1]-10,20,20)
    win.draw.rect((0,0,0),playerRect)
    win.draw.rect((200,50,50),apple)

    win.blit(count,(0,0))

    if pygwin.keyboard.isPressed('w'):
        player[1] -= 5
    if pygwin.keyboard.isPressed('s'):
        player[1] += 5
    if pygwin.keyboard.isPressed('d'):
        player[0] += 5
    if pygwin.keyboard.isPressed('a'):
        player[0] -= 5

    if player[0] <= -10:
        player[0] = 510
    if player[1] <= -10:
        player[1] = 510
    if player[0] > 510:
        player[0] = -10
    if player[1] > 510:
        player[1] = -10

    if playerRect.collide(apple):
        apple = pygwin.rect(random.randint(0,490),
                            random.randint(0,490),20,20)
        count += 1

    win.update(60)
pygwin.close()

```
