#Tutorial 2D game

import pygame 

pygame.init()


win = pygame.display.set_mode((500, 500))
#this line creates a window of 500W and 500h

pygame.display.set_caption("First Game")
#display the game name in the windows display

#Moving the Character

#charachter attributtes
x = 50
y = 50
width = 40
height = 60
vel = 5

run = True
is_jump = False
jump_count = 10

while run:
    pygame.time.delay(100) #this will delay the game the given amount o milliseconds, in this case, 0.1 seconds

    for event in pygame.event.get(): #This will loop through a list of any keyboard or mouse events. 
        if event.type == pygame.QUIT: #checks if the red button in the corner of the windows is clicked
            run = False #Ends the game loop

    keys = pygame.key.get_pressed() #this will give us a dictionary where each key has a vlaue of 1 or 0, where 1 is pressed and 0 isnt

    #we can check if a key is pressed like this

    if keys[pygame.K_LEFT] and x > vel: #setup boundaries so the top left position of the character is greater than our vel so we never move off screen
        x -= vel

    if keys[pygame.K_RIGHT] and x < 500 - vel - width: #setup boundaries so the top right corner of our character is less than the screen width - its width
        x += vel
    if not(is_jump): #Check if user is not jumping
        if keys[pygame.K_UP] and y > vel: #same aplly for the Y coordinate
            y -= vel

        if keys[pygame.K_DOWN] and y < 500 - vel - height:
            y += vel
        
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        #this is what will happen if we are jumping
        if jump_count >= -10:
            y -= (jump_count * abs(jump_count)) * 0.5
            jump_count -= 1
        else: #this will execute if our jump is finished 
            jump_count = 10
            is_jump = False
            #Resetting our variables


    win.fill((0,0,0)) #fills the screen with black so we dont keep track of the character last known position
    pygame.draw.rect(win, (255, 0 , 0), (x, y, width, height)) #This takes: windows/surface, color, rect
    pygame.display.update() #this updates the screen so we can see our rectangle

pygame.quit() #if we exit the loop this will execute and close our game

