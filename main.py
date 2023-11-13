import pygame
from sys import exit
from settings import *
from classes import *

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Cricket")
clock = pygame.time.Clock()

player = pygame.sprite.GroupSingle()
player.add(BATSMAN())

ball = pygame.sprite.GroupSingle()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        """
        if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                   ball.add(BALL())
        """

    screen.fill("Light Blue")

    player.draw(screen)
    player.update()
    ball.draw(screen)
    ball.update()

    pygame.display.update()
    clock.tick(60)