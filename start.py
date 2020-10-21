import pygame
import math
import random

pygame.init()
pygame.joystick.init()

# define the clock speed
clock = pygame.time.Clock()

# set Font
font = pygame.font.SysFont('Arial', 20, True)

# set screen parameters
screenWidth = 800
screenHeight = 500
screenName = "Psychedelic Encounters"

# define colors
WHITE = (255,255,255,255)
BLACK = (0,0,0,0)
RED = (255,0,0,255)
GREEN = (0,255,0,255)
BLUE = (0,0,255,0)

# make the window
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption(screenName)

class MotherEnemy(object):
    def __init__(self, cx, cy, radius, velx, vely, width, height):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.velx = velx
        self.vely = vely
        self.width = width
        self.height = height

    def ColissionDetection(self, px, py, pw, ph):
        if self.height <= 0:
            if px + pw > self.x - self.width and px < self.x + self.width and py + ph > self.y - self.width and py < self.y + self.width:
                return True
        else:
            #square hitbox.
            if py < self.y + self.height and (py + ph) > self.y and (px + pw) > self.x and px < self.x + self.width:
                return True

    def draw(self, win):
        if self.height <= 0:
            pygame.draw.circle(win, BLUE, (self.x, self.y), self.width)
        else:
            pygame.draw.rect(win, BLUE, (self.x, self.y, self.width, self.height))

class LinEnemy(MotherEnemy):
    def __init__(self, cx, cy, radius, velx, vely, width, height):
        super().__init__(cx, cy, radius, velx, vely, width, height)
        # define starting x and y
        self.x = self.cx
        self.y = self.cy

    def updateXY(self):
        if self.x >= (self.cx + self.radius) or self.x <= (self.cx - self.radius):
            self.velx *= (-1)
        self.x += self.velx

        if self.y >= (self.cy + self.radius) or self.y <= (self.cy - self.radius):
            self.vely *= (-1)
        self.y += self.vely

class DiaEnemy(MotherEnemy):
    def __init__(self, cx, cy, radius, velx, vely, width, height):
        super().__init__(cx, cy, radius, velx, vely, width, height)
        self.x = cx
        self.y = cy - radius

    def updateXY(self):
        if self.x == self.cx and self.y < self.cy:
            if self.velx < 0:
                self.velx *= (-1)
            if self.vely < 0:
                self.vely *= (-1)
        elif self.x > self.cx and self.y == self.cy:
            self.velx *= (-1)
        elif self.x == self.cx and self.y > self.cy:
            self.vely *= (-1)
        elif self.x < self.cx and self.y == self.cy:
            self.velx *= (-1)

        self.x += self.velx
        self.y += self.vely

class CirEnemy(MotherEnemy):
    def __init__(self, cx, cy, radius, velx, vely, width, height, direction):
        super().__init__(cx, cy, radius, velx, vely, width, height)
        self.x = cx + radius
        self.y = cy
        self.angle = 1
        if direction == 0:
            self.direction = 1 #clockwise
        elif direction == 1:
            self.direction = (-1) #anti-clockwise
        else:
            self.direction = 1
            print('Wrong direction given. Please state 0 for clockwise and 1 for anti-clockwise.')

    def updateXY(self):
        self.x = round(math.cos(self.angle * math.pi / 180) * self.radius) + self.cx
        self.y = round(math.sin(self.angle * math.pi / 180) * self.radius) + self.cy
        self.angle += self.direction * self.velx
        if self.angle >= 360 and self.direction == 1:
            self.angle = 0
        if self.angle <= 0 and self.direction == (-1):
            self.angle = 360

class player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.startx = x
        self.starty = y
        self.width = 20
        self.height = 20
        self.vel = 5
        self.level = 1

    def hit(self, active):
        if active:
            self.x = self.startx
            self.y = self.starty

    def win(self):
        self.level += 1
        for i in range(0, self.level):

            Rx = random.randint(200, 600) #x
            Ry = random.randint(150, 350) #y
            Rradius = random.randint(0, 200) #radius
            Rvelx = random.randint(1, 10) #velx
            Rvely = random.randint(1, 10)
            Rwidth = random.randint(5, 30)
            Rheight = random.randint(5, 30)

    #                              cx , cy , rad, velx,vely width height
            enemys.append(DiaEnemy(Rx, Ry, Rradius, Rvelx, Rvely, Rwidth, Rheight))

    def draw(self, win):
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))
        text = font.render(f'Level: {self.level}', 1, BLACK)
        win.blit(text, (705, 5))

class block(object):
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height
        self.active = True

    def draw(self, win):
        if self.active:
            pygame.draw.rect(win, RED, (self.x1, self.y1, self.width, self.height))
        else:
            pygame.draw.rect(win, GREEN, (self.x1, self.y1, self.width, self.height))

# Draw game window
def redrawGameWindow():
        win.fill(WHITE) # fill screen white
        start.draw(win) # draw start field
        finish.draw(win) # draw finish field

        # draw enemys
        for enemy in enemys:
            enemy.draw(win)

        player.draw(win) # draw player

        # everything done? Update the screen
        pygame.display.update()

def quitgame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

def mainLoop():
    global player
    global start
    global finish
    global enemys

    start = block(35, 390, 30, 30) # block(x, y, width, height)
    finish = block(735, 30, 30, 30) # block(x, y, width, height)
    player = player(40, 395) # player(x, y)

    enemys = []
    for i in range(0, player.level):

        Rx = random.randint(200, 600) #x
        Ry = random.randint(150, 350) #y
        Rradius = random.randint(0, 200) #radius
        Rvelx = random.randint(1, 10) #velx
        Rvely = random.randint(1, 10)
        Rwidth = random.randint(5, 30)
        Rheight = random.randint(5, 30)

#                              cx , cy , rad, velx,vely width height
        enemys.append(DiaEnemy(Rx, Ry, Rradius, Rvelx, Rvely, Rwidth, Rheight))
        #enemys.append(DiaEnemy(400, 250, 100, 1,   1,   10,   0))

    #                      cx,  cy,  rad, velx, vely, width, height, direction
    #enemys.append(CirEnemy(400, 250, 100, 1,    0,    20,    0,     1))

    #                      cx   cy   rad  velx vely width height
    #enemys.append(LinEnemy(400, 200, 200, 5,   0,   20,    10))
    #enemys.append(LinEnemy(40, 250, 240, 0, 10, 20, 10))

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_SPACE]:
            if keys[pygame.K_LEFT] and player.x > player.vel:
                    player.x -= player.vel
            if keys[pygame.K_RIGHT] and player.x < screenWidth - player.width - player.vel:
                    player.x += player.vel
            if keys[pygame.K_UP] and player.y > player.vel:
                    player.y -= player.vel
            if keys[pygame.K_DOWN] and player.y < screenHeight - player.height - player.vel:
                    player.y += player.vel
        else:
            # Joystick mechanics
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()

                # joystick axes for moving character
                for i in range(0, 1):
                    axisx = joystick.get_axis(0)
                    axisy = joystick.get_axis(1)
                    if axisx < -0.5  and player.x > player.vel:
                        player.x -= player.vel
                    if axisx > 0.5 and player.x < screenWidth - player.width - player.vel:
                        player.x += player.vel
                    if axisy < -0.5 and player.y > player.vel:
                        player.y -= player.vel
                    if axisy > 0.5 and player.y < screenHeight - player.height - player.vel:
                        player.y += player.vel

        for enemy in enemys:
            enemy.updateXY()
            if enemy.ColissionDetection(player.x, player.y, player.width, player.height):
                player.hit(start.active)

        # check for collision between player and start & finish
        if player.y < start.y2 and (player.y + player.width) > start.y1 and (player.x + player.width) > start.x1 and player.x < start.x2:
            start.active = False
        else:
            start.active = True
        # finish colission (and so you win)
        if player.y < finish.y2 and (player.y + player.width) > finish.y1 and (player.x + player.width) > finish.x1 and player.x < finish.x2:
            finish.active = False
            player.win()
            player.hit(start.active)
        else:
            finish.active = True

        redrawGameWindow()

mainLoop()
pygame.quit()
