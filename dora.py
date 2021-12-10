import pygame
from pygame import *
from random import randint

FPS = 60

screen = pygame.display.set_mode((600, 600))
screen.fill((255, 255, 255))

x = 200
y = 200


class Doors:

    def __init__(self):
        self.frame = pygame.image.load('pictures/1.png')
        self.door = pygame.image.load('pictures/3.png')
        self.y1 = 0
        self.cock = False
        self.dora_surface = pygame.Surface((40, 60))
        self.dora_surface.fill(0)
        self.dora_surface.blit(self.door, (0,0)) 

    def drawdoors(self, x, y):
        screen.blit(self.frame, (x, y))
        screen.blit(self.dora_surface, (x + 10, y + 10))
        #self.dora_surface.blit(self.door, (0,0)) 

            
    def opendoors(self):
        if self.cock:
            self.dora_surface.fill(0)
            self.dora_surface.blit(self.door, (0, self.y1))
            self.y1 -= 1
            if self.y1 < - 56:
                self.cock = False

    def cheycock(self):
        self.cock = True

finished = False
clock = pygame.time.Clock()

door1=Doors()
Doors = [door1]



while not finished:

    clock.tick(FPS)
    pygame.display.update()
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                door.cheycock()
        
    for door in Doors:
        door.opendoors()
        door.drawdoors(x, y)



pygame.quit()
