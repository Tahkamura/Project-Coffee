import pygame

pygame.init()

win = pygame.display.set_mode((1920,1080), pygame.RESIZABLE)
pygame.display.set_caption("Matiaksen peli")

x = 50
y = 50
width = 50
height = 50
vel = 5

run = True

while run:
    pygame.time.delay(20) # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay

    for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
        if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
            run = False  # Ends the game loop

    keys = pygame.key.get_pressed()  # This will give us a dictonary where each key has a value of 1 or 0. Where 1 is pressed and 0 is not pressed.

    if keys[pygame.K_LEFT] and x > vel: # We can check if a key is pressed like this
        x -= vel

    if keys[pygame.K_RIGHT] and x < 1540 - vel - width:
        x += vel

    if keys[pygame.K_UP] and y > vel:
        y -= vel

    if keys[pygame.K_DOWN] and y < 805 - height - vel:
        y += vel


    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255,255,0), (x, y, width, height))  #This takes: window/surface, color, rect 
    pygame.display.update() # This updates the screen so we can see our rectangle

pygame.quit()  # If we exit the loop this will execute and close our game
    
