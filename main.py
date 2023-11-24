import pygame
from sys import exit
from settings import *
from sprites import *

# for opaque surface
def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Cricket")
clock = pygame.time.Clock()

scoreboard = pygame.Surface((screen_width,scoreboard_height))
scoreboard.fill("#36454F")

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
        
        if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_UP:
                   ball.add(BALL())
        

    screen.blit(pitch,(0,0))

    player.draw(screen)
    player.update()
    computer.draw(screen)
    computer.update()
    
    ball.draw(screen)
    ball.update()

    screen.blit(scoreboard,(0,screen_height-scoreboard_height))
    
    pygame.display.update()
    clock.tick(60)