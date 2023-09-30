import pygame
from pygame_functions import *

pygame.init()

ww = 1000
wh = 650

window = pygame.display.set_mode((ww, wh))

clock = pygame.time.Clock()


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            pass

    window.fill((0, 0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()