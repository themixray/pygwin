import pygwin # Importing pygwin
import random # Importing random

win = pygwin.create('A Simple Game', (500,500)) # Creating window

player = [250,250] # Player position
apple = pygwin.rect(random.randint(0,490),
              random.randint(0,490),20,20) # Apple rect
score = 0 # Player score

run = True # Is loop running
while run: # Creating loop
    for event in pygwin.getEvents(): # Events loop
        if event.type == pygwin.QUIT: # If window quit
            run = False # Break loop
    win.fill((255,255,255)) # Fill window with color

    playerRect = pygwin.rect(player[0]-10,player[1]-10,20,20) # Player rect
    win.draw.rect((0,0,0),playerRect) # Drawing player rect
    win.draw.rect((200,50,50),apple) # Drawing apple rect

    win.blit(score,(0,0)) # Writing player score

    if pygwin.keyboard.isPressed('w'): # If keyboard key w pressed
        player[1] -= 5 # Player position up
    if pygwin.keyboard.isPressed('s'): # If keyboard key s pressed
        player[1] += 5 # Player position down
    if pygwin.keyboard.isPressed('d'): # If keyboard key d pressed
        player[0] += 5 # Player position right
    if pygwin.keyboard.isPressed('a'): # If keyboard key a pressed
        player[0] -= 5 # Player position left

    if player[0] <= -10: # If player out of the screen (left)
        player[0] = 510 # Set player position in right
    if player[1] <= -10: # If player out of the screen (up)
        player[1] = 510 # Set player position in down
    if player[0] > 510: # If player out of the screen (right)
        player[0] = -10 # Set player position in left
    if player[1] > 510: # If player out of the screen (down)
        player[1] = -10 # Set player position in up

    if playerRect.collide(apple): # If player rect collide apple rect
        apple = pygwin.rect(random.randint(0,490),
                      random.randint(0,490),20,20) # Change apple rect
        score += 1 # Update player score

    win.update(60) # Update window
pygwin.close() # Close pygwin
