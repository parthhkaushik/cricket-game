import pygame
from settings import *
from sprites import *

# intialise pygame
pygame.init()

# scoreboard
def display_score():
     scoreboard = pygame.Surface((screen_width,scoreboard_height))
     scoreboard.fill("#36454F")
     screen.blit(scoreboard,(0,screen_height-scoreboard_height))

# game starts when it is True
game_active = True

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

pygame.display.set_caption("Cricket")

# rendering the pitch
pitch = pygame.image.load('graphics/background.jpg').convert()
pitch = pygame.transform.scale(pitch, (screen_width, screen_height))

umpire = pygame.image.load("graphics/umpire.png")
umpire = pygame.transform.scale(umpire, (80,215))

# adding the player and computer sprites
player = pygame.sprite.GroupSingle()
player.add(BATSMAN())
computer = pygame.sprite.GroupSingle()
computer.add(BOWLER())

ball = pygame.sprite.GroupSingle()

# game loop
while True:
    # 60 frames per second
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == THROW_BALL:
               ball.add(BALL())
    
    # checking for game active condition
    if game_active:
        screen.blit(pitch,(0,0))

        # drawing the sprites
        player.draw(screen)
        computer.draw(screen)
        ball.draw(screen)

        screen.blit(umpire,(screen_width/2-35,340))

        # updating the sprites
        player.update()
        computer.update()
        ball.update()

        # displaying the sccoreboard
        display_score() 
        
    else:
        # main menu
        pass
    
    # updating display
    pygame.display.update()