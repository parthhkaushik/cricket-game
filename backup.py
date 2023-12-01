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
timing = 3

def check_runs_scored():
    dr = abs(BOWLER.t_ball_released-BATSMAN.t_player_input)
    if 80 <= dr <= 100:
        global runs_scored
        runs_scored = 6
        BATSMAN.shot = "loft"
        global timing
        timing = 3
    elif 60 <= dr <= 120:
        runs_scored = 4
        BATSMAN.shot = "stroke"
        timing = 2
    else:
        BATSMAN.shot = "stroke"
        timing = 1
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
batsman = pygame.sprite.GroupSingle()
batsman.add(BATSMAN())
non_striker = pygame.sprite.GroupSingle()
non_striker.add(NON_STRIKER())

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
dt = 0
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, THROW_BALL])
while True:
    # 60 frames per second
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
             exit()
        elif event.type == THROW_BALL:
             ball.add(BALL())
             NON_STRIKER.can_move = True                 
        elif event.type == pygame.KEYDOWN and not game_active:
             game_active = True   
    
    # checking for game active condition
    if game_active:
        screen.blit(pitch,(0,0))
        screen.blit(wickets,(screen_width/2-15,105))

        # other objects
        screen.blit(pause,(screen_width-80-10,10))
        blit_alpha(screen, logo, (20,20), 128)

        # player and computer sprites
        batsman.draw(screen)
        batsman.update()
        bowler.draw(screen)
        bowler.update()        
        screen.blit(umpire,(screen_width/2-35,340))
        non_striker.draw(screen)
        non_striker.update()

        ball.draw(screen)
        ball.update()
        
        # displaying the sccoreboard
        SCOREBOARD().display_score(screen) 
        TIMING_BAR().blit(screen)

        if BATSMAN.key_pressed:
            check_runs_scored()
            batsman.sprite.updated()
            BATSMAN.key_pressed = False
            flag = 1 
        else:
            flag = 0

        if BATSMAN.delivery_played:
             dt+=1
             TIMING_BAR().update(screen,timing)  
             if dt >= 120: 
                 display_runs(runs_scored,screen)    
                                  
        else:
            dt = 0

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