import pygame, random
from settings import *
from module import blit_alpha

# importing sprites
from sprites.batsman import *
from sprites.bowler import *

# intialise pygame
pygame.init()


class GAME():
    runs_scored,dr = 0,0
    
    # images
    pitch = pygame.image.load('graphics/background.jpg')
    pitch = pygame.transform.scale(pitch,(screen_width,screen_height))

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
        GAME.ball.draw(target)
        GAME.ball.update()

        GAME.all_sprites.draw(target)
        for sprite in GAME.all_sprites.sprites():
            sprite.update()
        target.blit(GAME.umpire,umpire_pos)
                
        # displaying the sccoreboard
        SCOREBOARD().display_score(target) 

        if BATSMAN.key_pressed:
            GAME.check_runs_scored()
            GAME.all_sprites.sprites()[0].shot_select()
            BALL.shot = BATSMAN.shot
            BALL.delivery_played = True
            BATSMAN.key_pressed = False

        if BATSMAN.display_runs: display_runs(GAME.runs_scored,target)  

    def check_runs_scored():
        GAME.dr = BATSMAN.t_player_input-BOWLER.t_ball_released

        if BATSMAN.direction == BALL.direction:

            if 40 <= GAME.dr <= 100:
                GAME.runs_scored = 6
                BATSMAN.shot = "loft"
            
            elif 20 <= GAME.dr <= 120:
                GAME.runs_scored = "Catch-Out"
                BATSMAN.shot = "loft"

            elif 0 <= GAME.dr <= 140:
                GAME.runs_scored = 4
                BATSMAN.shot = "stroke"

            elif -200 <= GAME.dr <= 200:
                BATSMAN.shot = "stroke"
                GAME.runs_scored = random.choice([1,1,1,2,2,3])
            
            else: GAME.check_wicket()

        else:
            GAME.check_wicket() 

    def check_wicket():

        if BALL.direction != "straight":

            if -220 <= GAME.dr <= 220 and BATSMAN.direction == BALL.direction:
                GAME.runs_scored = "Caught"
            else: 
                GAME.runs_scored = 0
                BALL.delivery_played = True
        
        else: GAME.runs_scored = "Bowled"
            
        
        