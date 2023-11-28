import pygame
from settings import *
from sprites import *

# intialise pygame
pygame.init()

def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

# scoreboard
def display_score():
    scoreboard = pygame.Surface((screen_width,scoreboard_height))
    scoreboard.fill("#343434")
    screen.blit(scoreboard,(0,screen_height-scoreboard_height))

# game starts when it is True
game_active = False

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

pygame.display.set_caption("Cricket 2023")

img = pygame.image.load("graphics/home-screen.png")
img = pygame.transform.scale(img,(screen_width,screen_height))
font = pygame.font.Font("fonts/Aller_Rg.ttf",25)

# rendering the pitch
pitch = pygame.image.load('graphics/background.jpg').convert()
pitch = pygame.transform.scale(pitch,(screen_width,screen_height))

umpire = pygame.image.load("graphics/umpire.png")
umpire = pygame.transform.scale(umpire,(80,215))
wickets = pygame.image.load("graphics/wickets.png")
wickets = pygame.transform.scale(wickets,(40,80))

pause = pygame.image.load("graphics/pause.png")
pause = pygame.transform.scale(pause,(80,30))
logo = pygame.image.load("graphics/logo.png")

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
        if event.type == pygame.KEYDOWN and not game_active:
                game_active = True
    
    # checking for game active condition
    if game_active:
        screen.blit(pitch,(0,0))
        screen.blit(wickets,(screen_width/2-15,105))

        screen.blit(pause,(screen_width-80-10,10))
        blit_alpha(screen, logo, (20,20), 128)

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
        screen.blit(img,(0,0))

        message = font.render("PRESS ANY KEY TO CONTINUE",False,(0,0,0))
        message_rect = message.get_rect(center = (425,screen_height-20))
        screen.blit(message,message_rect)
    
    # updating display
    pygame.display.update()