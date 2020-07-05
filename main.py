import pygame
import random
import os
import pygame

# WINDOWS POSITION
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
roundBulletImg = pygame.image.load('roundBullet0.png')


# Enemy class
class Enemy:
    def __init__(self, type, pos):
        if type == 1:
            self.img = enemy1Img
        elif type == 2:
            self.img = enemy2Img
        self.original_pos = pos  # main position
        self.pos_x = pos  # current position
        self.pos_y = 1000
        self.point = 0  # moving parameter. Where the enemy have to go (x)
        self.speed = 0  # moving parameter. Will change from time to time
        self.goBack = False  # moving parameter. True if enemy reached the point and have to go back

    def starting(self, speedY):
        self.pos_y -= speedY

    # needs completely rewriting. ...maybe?
    # Спершу генерується точка, до якої має рухатись ворог, та його швидкість.
    def move(self):
        if self.point == 0:
            self.point = random.randint(-60, 60)
            print(self.point)
            self.speed = random.uniform(0.03, 0.1)
        if not self.goBack:  # ворог рухається до точки
            if self.point < 0:
                self.pos_x -= self.speed
            else:
                self.pos_x += self.speed
            if self.point < 0:  # перевірка, чи ворог дійшов до точки. Якщо так, goBack = True
                if (self.pos_x - self.original_pos) < self.point:
                    self.goBack = True
            else:
                if (self.pos_x - self.original_pos) > self.point:
                    self.goBack = True
        else:  # ворог повертається
            if self.point < 0:
                self.pos_x += self.speed
                if self.pos_x > self.original_pos:  # перевірка, чи ворог повернувся на початкову позицію
                    self.pos_x = self.original_pos
                    self.point = 0
                    self.speed = 0
                    self.goBack = False
            else:
                self.pos_x -= self.speed
                if self.pos_x < self.original_pos:  # така ж перевірка
                    self.pos_x = self.original_pos
                    self.point = 0
                    self.speed = 0
                    self.goBack = False

    def visualise(self):
        screen.blit(self.img, (round(self.pos_x), round(self.pos_y)))

    def shooting(self, speed=0.001, type=1):
        bullets.append(Bullet(self, speed, type))  # у список з пулями додається нова


# Bullet class
class Bullet:
    def __init__(self, enemy, speed, type):
        self.angle = 0
        self.speed_x = (player_x - enemy.pos_x) / (1 / speed)  # !!! Need rewriting!!! Bullets are slower !!!
        self.speed_y = (player_y - enemy.pos_y) / (1 / speed)  # !!! when player are closer!              !!!
        self.type = type
        self.time = 3000
        self.pos_x = enemy.pos_x
        self.pos_y = enemy.pos_y

    def visualise(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        screen.blit(roundBulletImg, (round(self.pos_x), round(self.pos_y)))


# Player
player_x = 484
player_y = 740
player_left = 0
player_right = 0
player_up = 0
player_down = 0


def player(x, y):
    screen.blit(playerImg, (round(x), round(y)))


# GAME PREPARING
r = 35
g = 35
b = 80
lockR = False
lockG = False
running = True
starting = True
bullets = []
enemy = [Enemy(1, 134), Enemy(2, 384), Enemy(2, 584), Enemy(1, 834)]

startingPlayerY = 740
s = pygame.Surface((1000, 800))  # the size of your rect
s.set_alpha(128)  # alpha level
s.fill((r, g, b))  # this fills the entire surface
# GAME STARTING
while starting:
    # screen.blit(background, (0, 0))
    screen.fill((r, g, b))
    # screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates

    if enemy[0].pos_y > 630:
        for each in enemy:
            each.starting(0.2)
    else:
        starting = False

    if player_y > 300:
        player_y -= 0.3

    for each in enemy:
        each.move()

    for each in enemy:
        each.visualise()
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

    for each in enemy:
        each.move()

    for each in enemy:
        each.visualise()

    for each in enemy:
        if random.random() < 0.005:
            each.shooting()

    for each in bullets:
        each.visualise()

    player(player_x, player_y)

    pygame.display.update()
