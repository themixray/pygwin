from win32api import GetSystemMetrics # Importing monitor resolution getter
import pygwin
import random
import copy

win = pygwin.create('A Simple Game', (500,500))
win.move(*[int(GetSystemMetrics(i)/2-win.size[i]/2) for i in range(2)]) # Center window
centered_position = win.position # Get centered position of window

player = [250,250]
apple = pygwin.rect(random.randint(0,490),
              random.randint(0,490),20,20)
score = 0

run = True
while run:
    for event in pygwin.getEvents():
        if event.type == pygwin.QUIT:
            run = False
    win.fill((255,255,255))

    playerRect = pygwin.rect(player[0]-10,player[1]-10,20,20)
    playerRect.x += centered_position[0]-win.position[0] # Set player rect x pos relatively center of monitor
    playerRect.y += centered_position[1]-win.position[1] # Set player rect y pos relatively center of monitor
    win.draw.rect((0,0,0),playerRect)
    atemp = copy.copy(apple) # Create copy of apple rect
    atemp.x += centered_position[0]-win.position[0] # Set apple x pos relatively center of monitor
    atemp.y += centered_position[1]-win.position[1] # Set apple y pos relatively center of monitor
    win.draw.rect((200,50,50),atemp)

    win.blit(score,(0,0))

    set_position = win.position
    if pygwin.keyboard.isPressed('w'):
        player[1] -= 5
        set_position[1] -= 5 # Move window up
    if pygwin.keyboard.isPressed('s'):
        player[1] += 5
        set_position[1] += 5 # Move window down
    if pygwin.keyboard.isPressed('d'):
        player[0] += 5
        set_position[0] += 5 # Move window right
    if pygwin.keyboard.isPressed('a'):
        player[0] -= 5
        set_position[0] -= 5 # Move window left
    win.move(*set_position) # Set position

    if playerRect.collide(apple):
        apple = pygwin.rect(random.randint(50,490),
                      random.randint(50,490),20,20)
        score += 1

    win.update(60)
pygwin.close()
