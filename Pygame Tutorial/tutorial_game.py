#Tutorial 2D game

import pygame 

pygame.init()


win = pygame.display.set_mode((500, 480))
#this line creates a window of 500W and 500h

pygame.display.set_caption("First Game")
#display the game name in the windows display

#importing the images
walk_right = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walk_left = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

#Setting the framerate to 27
clock = pygame.time.Clock()

#Player Class
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.right = False
        self.left = False
        self.walk_count = 0
        self.jump_count = 10
        self.standing = True
    
    def draw(self, win):
        # We have 9 images for our walking animation, I want to show the same image for 3 frames
        # so I use the number 27 as an upper bound for walkCount because 27 / 3 = 9. 
        # 9 images shown, 3 times each animation.

        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not(self.standing):
            if self.left:
                win.blit(walk_left[self.walk_count//3], (self.x, self.y)) #we integer divide walk_count by 3 to ensure each
                self.walk_count += 1 #image is shown 3 times every animation

            elif self.right:
                win.blit(walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1

        else: #if the character is standing still
            if self.right:
                win.blit(walk_right[0], (self.x, self.y))
            else:
                win.blit(walk_left[0], (self.x, self.y))


#Projectile Class
class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

#Redrawing the game window - Main function
def redraw_game_window():
    win.blit(bg, (0,0)) #this will draw the bg image at (0,0)
    man.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


#Main Loop
man = player(200, 410, 64, 64)
run = True
bullets = []
while run:
    clock.tick(27)

    for event in pygame.event.get(): #This will loop through a list of any keyboard or mouse events. 
        if event.type == pygame.QUIT: #checks if the red button in the corner of the windows is clicked
            run = False #Ends the game loop
    
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel #moves the bullet by its vel
        else:
            bullets.pop(bullets.index(bullet)) #This will remove the bullet if its off screen

    keys = pygame.key.get_pressed() #this will give us a dictionary where each key has a vlaue of 1 or 0, where 1 is pressed and 0 isnt

    #we can check if a key is pressed like this

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        
        if len(bullets) < 5: #this will limit the bullets per 5 on screen at a time
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
            #this will shoot a bullet from the middle of the character

    if keys[pygame.K_LEFT] and man.x > man.vel: #setup boundaries so the top left position of the character is greater than our vel so we never move off screen
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < 480 - man.vel - man.width: #setup boundaries so the top right corner of our character is less than the screen width - its width
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False

    else: #if the character is not moving it will set STANDING = TRUE and reset the animation counter (walk_count)
        man.standing = True
        man.walk_count = 0

    if not(man.is_jump): #Check if user is not jumping
        if keys[pygame.K_UP]:
            man.is_jump = True
            man.left = False
            man.right = False
            man.walk_count = 0
    else:
        #this is what will happen if we are jumping
        if man.jump_count >= -10:
            neg = 1
            if man.jump_count < 0:
                neg = -1
            man.y -= (man.jump_count ** 2) * 0.5 * neg
            man.jump_count -= 1

        else: #this will execute if our jump is finished 
            man.jump_count = 10
            man.is_jump = False
            #Resetting our variables


    redraw_game_window()

pygame.quit() #if we exit the loop this will execute and close our game

