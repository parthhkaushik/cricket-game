import pygame, random
from settings import *
from module import *

# importing sprites
from sprites.batsman import *
from sprites.bowler import *

# intialise pygame
pygame.init()

# variables
runs_scored = 0
flag = 0

def check_runs_scored():
    if BATSMAN.delivery_played:
        dr = abs(t_ball_released-t_player_input)
        if dr <= 20:
            global runs_scored
            runs_scored = 6
        elif dr <= 25:
            runs_scored = 4
        else:
            global flag
            if not flag: 
                runs_scored = random.choice([1,1,1,2,2,3])
                flag = 0

# game starts when it is True
game_active = True

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

pygame.display.set_caption("Cricket 2023")

# adding the sprites
batsman_group = pygame.sprite.Group()
batsman_group.add(BATSMAN())
batsman_group.add(NON_STRIKER())

umpire = pygame.image.load("graphics/umpire.png")
umpire = pygame.transform.scale(umpire,(80,215))

bowler = pygame.sprite.GroupSingle()
bowler.add(BOWLER())
ball = pygame.sprite.GroupSingle()

# home-screen image
img = pygame.image.load("graphics/home-screen.png")
img = pygame.transform.scale(img,(screen_width,screen_height))

# loading the pitch
pitch = pygame.image.load('graphics/background.jpg').convert()
pitch = pygame.transform.scale(pitch,(screen_width,screen_height))
wickets = pygame.image.load("graphics/wickets.png")
wickets = pygame.transform.scale(wickets,(40,80))

# adding other objects
pause = pygame.image.load("graphics/pause.png")
pause = pygame.transform.scale(pause,(80,30))
logo = pygame.image.load("graphics/logo.png")


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
                NON_STRIKER.can_move = True              
        if event.type == pygame.KEYDOWN and not game_active:
                game_active = True
    
    # checking for game active condition
    if game_active:
        screen.blit(pitch,(0,0))
        screen.blit(wickets,(screen_width/2-15,105))

        screen.blit(pause,(screen_width-80-10,10))
        blit_alpha(screen, logo, (20,20), 128)

        bowler.draw(screen)
        bowler.update()        
        batsman_group.draw(screen)
        batsman_group.update()

        screen.blit(umpire,(screen_width/2-35,340))
        
        ball.update()
        ball.draw(screen)
        
        # displaying the sccoreboard
        SCOREBOARD().display_score(screen)
        check_runs_scored() 
        if BATSMAN.delivery_played: 
             display_runs(runs_scored,screen)
             flag = 1
        else: flag = 0
    
    else:
        # main menu
        screen.blit(img,(0,0))

        # message
        PROGRESS_BAR().load(screen,(175,screen_height-30),(450,10))
        if not PROGRESS_BAR.loading:
            message = "PRESS ANY KEY TO CONTINUE"
            pos = (screen_width/2+15,screen_height-30)
            TEXT().blit(message,screen,pos,bounce=True)   
            
    
    # updating display
    pygame.display.update()