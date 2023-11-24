import pygame
from sys import exit
from settings import *
from sprites import *

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Cricket")
clock = pygame.time.Clock()

pitch = pygame.image.load('graphics/background.jpg').convert()
pitch = pygame.transform.scale(pitch, (screen_width, screen_height))

player = pygame.sprite.GroupSingle()
player.add(BATSMAN())

computer = pygame.sprite.GroupSingle()
computer.add(BOWLER())

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

    screen.blit(pitch,(0,0))

    player.draw(screen)
    player.update()
    computer.draw(screen)
    computer.update()

    """
    ball.draw(screen)
    ball.update()
    """
    pygame.display.update()
    clock.tick(60)