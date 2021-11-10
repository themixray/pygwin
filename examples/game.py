from random import randint
import pygwin as pgw

win = pgw.create('Game Example', (500,500))

player = [250,250]
apple = pgw.rect(randint(0,490),randint(0,490),20,20)
count = 0

run = True
while run:
    for event in pgw.getEvents():
        if event.type == pgw.QUIT:
            run = False
    win.fill((255,255,255))
    playerRect = pgw.rect(player[0]-10,player[1]-10,20,20)
    win.draw.rect((0,0,0),playerRect)
    win.draw.rect((200,50,50),apple)
    win.blit(count,(0,0))
    if pgw.keyboard.isPressed('w'):
        player[1] -= 5
    if pgw.keyboard.isPressed('s'):
        player[1] += 5
    if pgw.keyboard.isPressed('d'):
        player[0] += 5
    if pgw.keyboard.isPressed('a'):
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
        apple = pgw.rect(randint(0,490),randint(0,490),20,20)
        count += 1
    win.update(60)
pgw.close()
