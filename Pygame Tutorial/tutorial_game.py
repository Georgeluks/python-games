#Tutorial 2D game

import pygame 

pygame.init()


win = pygame.display.set_mode((500, 480))
#this line creates a window of 500W and 500h

pygame.display.set_caption("First Game")
#display the game name in the windows display

# Global Variables
score = 0
font = pygame.font.SysFont("comicsans", 30, True) 

#loading the sounds
bullet_sound = pygame.mixer.Sound("bullet.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

music = pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)

#loading the images
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
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) #this elements are: top left x, top left y, width, height
    
    def hit(self):
        self.x = 60
        self.y = 410
        self.walk_count = 0 
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
    
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
            
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

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

#Enemies Class
class enemy(object):
    #import enemies animation
    walk_right = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walk_left = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end] #This will define where the enemy starts and finishes his path
        self.walk_count = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 10
        self.visible = True
    
    def move(self):
        if self.vel > 0: #if we are moving right
            if self.x < self.path[1] + self.vel: #if we`ve not reached the furthest right point on our path
                self.x += self.vel
            else: #Change direction
                self.vel= self.vel * -1
                self.x += self.vel
                self.walk_count = 0
        else: #IF we are moving left
            if self.x > self.path[0] - self.vel: #if we have not reached the furthest left point on our path
                self.x += self.vel
            else: #change direction
                self.vel = self.vel * -1
                self.x += self.vel
                self.walk_count = 0
    
    def hit(self):
        hit_sound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("hit")
    
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 33: #33 because the enemies have 11 images for each animation, each image for 3 frames > 3 x 11 = 22
                self.walk_count = 0

            if self.vel > 0: #if we are moving to the right we will display  our walk_right images
                win.blit(self.walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            else: #otherwise we will display our walk_left images
                win.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 *(10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

#Redrawing the game window - Main function
def redraw_game_window():
    win.blit(bg, (0,0)) #this will draw the bg image at (0,0)
    man.draw(win)
    goblin.draw(win)
    text = font.render("Score: " + str(score), 1, (0,0,0))
    win.blit(text, (390, 10))

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


#Main Loop
man = player(200, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 300)
run = True
bullets = []
shoot_loop = 0

while run:
    clock.tick(27)

    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            man.hit()
            score -= 5

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 5:
        shoot_loop = 0

    for event in pygame.event.get(): #This will loop through a list of any keyboard or mouse events. 
        if event.type == pygame.QUIT: #checks if the red button in the corner of the windows is clicked
            run = False #Ends the game loop
    
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:# Checks x coords
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]: #checks y coords
                goblin.hit() #calls enemy hit method
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel #moves the bullet by its vel
        else:
            bullets.pop(bullets.index(bullet)) #This will remove the bullet if its off screen

    keys = pygame.key.get_pressed() #this will give us a dictionary where each key has a vlaue of 1 or 0, where 1 is pressed and 0 isnt

    #we can check if a key is pressed like this

    if keys[pygame.K_SPACE] and shoot_loop == 0:
        bullet_sound.play()
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

