import pygame
import random
import os
import pygame

x = 100
y = 45
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
pygame.init()
screen = pygame.display.set_mode((100, 100))

# init pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1000, 720))

# title & icon
pygame.display.set_caption("Surviving is highly recommended!")
icon = pygame.image.load('RP.png')
pygame.display.set_icon(icon)

# Images
playerImg = pygame.image.load('you.png')
enemy1Img = pygame.image.load('enemy1.png')
enemy2Img = pygame.image.load('enemy2.png')
asteroid1Img = pygame.image.load('asteroid1.png')
asteroid2Img = pygame.image.load('asteroid2.png')
asteroid3Img = pygame.image.load('asteroid3.png')
background = pygame.image.load('space.png')
bulletImg = pygame.image.load('bullet.png')


# Enemy class
class Enemy:
    def __init__(self, type, pos):
        if type == 1:
            self.img = enemy1Img
        else:
            self.img = enemy2Img
        self.original_pos = pos
        self.pos_x = pos
        self.point = 0
        self.speed = 0
        self.goBack = False
        self.pos_y = 1000

    def starting(self, speedY):
        self.pos_y -= speedY

    # needs completely rewriting. ...maybe?
    def move(self):
        if self.point == 0:
            self.point = random.randint(-60, 60)
            print(self.point)
            self.speed = random.uniform(0.03, 0.1)
        if not self.goBack:
            if self.point < 0:
                self.pos_x -= self.speed
            else:
                self.pos_x += self.speed
            if self.point < 0:
                if (self.pos_x - self.original_pos) < self.point:
                    self.goBack = True
            else:
                if (self.pos_x - self.original_pos) > self.point:
                    self.goBack = True
        else:
            if self.point < 0:
                self.pos_x += self.speed
                if self.pos_x > self.original_pos:
                    self.pos_x = self.original_pos
                    self.point = 0
                    self.speed = 0
                    self.goBack = False
            else:
                self.pos_x -= self.speed
                if self.pos_x < self.original_pos:
                    self.pos_x = self.original_pos
                    self.point = 0
                    self.speed = 0
                    self.goBack = False

    def visualise(self):
        screen.blit(self.img, (self.pos_x, self.pos_y))

    def shooting(self):
        bullets.append(Bullet(self))

class Bullet:
    def __init__(self, enemy, speed = 0.002, type = 1):
        self.angle = 0
        self.speed_x = (player_x - enemy.pos_x) / (1/speed)
        self.speed_y = (player_y - enemy.pos_y) / (1/speed)
        self.type = type
        self.time = 1000
        self.pos_x = enemy.pos_x
        self.pos_y = enemy.pos_y

    def visualise(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        screen.blit(bulletImg, (self.pos_x, self.pos_y))






# Player
player_x = 484
player_y = 740
player_left = 0
player_right = 0
player_up = 0
player_down = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# GAME PREPARING
r = 35
g = 35
b = 80
lockR = False
lockG = False
running = True
starting = True
bullets = []
enemy1 = Enemy(1, 134)
enemy2 = Enemy(2, 384)
enemy3 = Enemy(2, 584)
enemy4 = Enemy(1, 834)
startingPlayerY = 740
s = pygame.Surface((1000, 800))  # the size of your rect
s.set_alpha(128)  # alpha level
s.fill((r, g, b))  # this fills the entire surface
# GAME STARTING
while starting:
    # screen.blit(background, (0, 0))
    screen.fill((r, g, b))
    # screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates

    if enemy1.pos_y > 630:
        enemy1.starting(0.2)
        enemy2.starting(0.2)
        enemy3.starting(0.2)
        enemy4.starting(0.2)
    else:
        starting = False

    if player_y > 300:
        player_y -= 0.3

    enemy1.move()
    enemy2.move()
    enemy3.move()
    enemy4.move()
    enemy1.visualise()
    enemy2.visualise()
    enemy3.visualise()
    enemy4.visualise()
    player(player_x, player_y)

    pygame.display.update()




# GAME RUNNING
while running:
    # background R
    if not lockR:
        r += 0.005
    else:
        r -= 0.004
        if r < 20:
            lockR = False
    if r > 55:
        lockR = True
    # background G
    if not lockG:
        g += 0.007
    else:
        g -= 0.012
        if g < 30:
            lockG = False
    if g > 50:
        lockG = True
    # screen
    screen.fill((r, g, b))
    # screen.blit(background, (0, 0))
    # s.fill((r, g, b))
    # screen.blit(s, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_left = 0.3
            if event.key == pygame.K_RIGHT:
                player_right = 0.3
            if event.key == pygame.K_UP:
                player_up = 0.3
            if event.key == pygame.K_DOWN:
                player_down = 0.3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_left = 0
            if event.key == pygame.K_RIGHT:
                player_right = 0
            if event.key == pygame.K_UP:
                player_up = 0
            if event.key == pygame.K_DOWN:
                player_down = 0

    player_x += player_right
    player_x -= player_left
    player_y += player_down
    player_y -= player_up

    if player_x <= 0:
        player_x = 0
    if player_x >= 968:
        player_x = 968
    if player_y <= 50:
        player_y = 50
    if player_y >= 450:
        player_y = 450

    enemy1.move()
    enemy2.move()
    enemy3.move()
    enemy4.move()

    enemy1.visualise()
    enemy2.visualise()
    enemy3.visualise()
    enemy4.visualise()

    chance1 = random.randint(0, 500)
    chance2 = random.randint(0, 500)
    chance3 = random.randint(0, 500)
    chance4 = random.randint(0, 500)
    if chance1 > 498:
        enemy1.shooting()
    if chance2 > 498:
        enemy2.shooting()
    if chance3 > 498:
        enemy3.shooting()
    if chance4 > 498:
        enemy4.shooting()

    for each in bullets:
        each.visualise()

    player(player_x, player_y)

    pygame.display.update()
