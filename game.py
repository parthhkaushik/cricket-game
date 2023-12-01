import pygame, random
from settings import *
from module import blit_alpha

# importing sprites
from sprites.batsman import *
from sprites.bowler import *

# intialise pygame
pygame.init()

# variables
runs_scored = 0

def check_runs_scored():
    dr = abs(BOWLER.t_ball_released-BATSMAN.t_player_input)
    if 80 <= dr <= 100:
        global runs_scored
        runs_scored = 6
        BATSMAN.shot = "loft"
    elif 60 <= dr <= 120:
        runs_scored = 4
        BATSMAN.shot = "stroke"
    else:
        BATSMAN.shot = "stroke"
        runs_scored = random.choice([1,1,1,2,2,3])


class GAME():
    pitch = pygame.image.load('graphics/background.jpg')
    pitch = pygame.transform.scale(pitch,(screen_width,screen_height))
    
    # images
    logo = pygame.image.load("graphics/logo.png")
    pause = pygame.image.load("graphics/pause.png")
    pause = pygame.transform.scale(pause,(80,30))

    umpire = pygame.image.load("graphics/umpire.png")
    umpire = pygame.transform.scale(umpire,(80,215))
    
    wickets = pygame.image.load("graphics/wickets.png")
    wickets = pygame.transform.scale(wickets,(40,80))

    # sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(BATSMAN(),NON_STRIKER(),BOWLER())
    ball = pygame.sprite.GroupSingle()

    def RUN(self, target):

        target.blit(GAME.pitch,(0,0))
        target.blit(GAME.wickets,(screen_width/2-15,105))

        # other objects
        target.blit(GAME.pause,(screen_width-80-10,10))
        blit_alpha(target, GAME.logo, (20,20), 128)

        # player and computer sprites
        GAME.all_sprites.draw(target)
        for sprite in GAME.all_sprites.sprites():
            sprite.update()

        GAME.ball.draw(target)
        GAME.ball.update()
        target.blit(GAME.umpire,umpire_pos)
                
        # displaying the sccoreboard
        SCOREBOARD().display_score(target) 

        if BATSMAN.key_pressed:
            check_runs_scored()
            GAME.all_sprites.sprites()[0].updated()
            BATSMAN.key_pressed = False

        if BATSMAN.display_runs: display_runs(runs_scored,target)                      