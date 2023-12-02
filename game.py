import pygame, random
from settings import *
from module import *

# importing sprites
from sprites.ball import *
from sprites.batsman import *
from sprites.bowler import *
from sprites.nonstriker import *


class GAME():

    # variables
    next_ball_event = False
    dt,dr = 0,0
    total_overs = ""
    runs_scored = 0
    show_circle = False
    
    # images
    pitch = pygame.image.load('graphics/background.jpg')
    pitch = pygame.transform.scale(pitch,(screen_width,screen_height))

    logo = pygame.image.load("graphics/logo.png")
    pause = pygame.image.load("graphics/pause.png")
    pause = pygame.transform.scale(pause,(80,30))

    umpire = pygame.image.load("graphics/umpire.png")
    umpire = pygame.transform.scale(umpire,(80,215))
    
    wickets = pygame.image.load("graphics/wickets-1.png")
    wickets = pygame.transform.scale(wickets,(64,80))

    circle = pygame.image.load("graphics/target.png")
    circle = pygame.transform.scale(circle,(30,15))

    # sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(BATSMAN(),NON_STRIKER(),BOWLER())
    ball = pygame.sprite.GroupSingle()

    def RUN(self, target):

        target.blit(GAME.pitch,(0,0))
        target.blit(GAME.wickets,(screen_width/2-25,105))

        # other objects
        target.blit(GAME.pause,(screen_width-80-10,10))
        blit_alpha(target, GAME.logo, (20,20), 128)

        # player and computer sprites
        GAME.all_sprites.draw(target)
        for sprite in GAME.all_sprites.sprites():
            sprite.update()
        target.blit(GAME.umpire,umpire_pos)
        
        if GAME.show_circle: target.blit(GAME.circle,BALL.circle_pos)

        GAME.ball.draw(target)
        GAME.ball.update()
                
        # displaying the sccoreboard
        SCOREBOARD().blit(target, GAME.total_overs) 

        GAME.dt += 1
        if GAME.dt >= 420:
            if not BATSMAN.delivery_played: GAME.check_wicket()
            GAME.display_runs(GAME.runs_scored,target) 

        if GAME.next_ball_event:
            BATSMAN.next_ball_event = True
            BOWLER.next_ball_event = True
            NON_STRIKER.next_ball_event = True
            GAME.dt = 0
            SCOREBOARD().update(GAME.runs_scored, GAME.total_overs)
            GAME.next_ball_event = False
            GAME.show_circle = False

        if BATSMAN.key_pressed:
            GAME.check_runs_scored()
            GAME.all_sprites.sprites()[0].play_shot()
            BALL.shot = BATSMAN.shot
            BALL.delivery_played = True
            BATSMAN.key_pressed = False 
                

    """ methods """

    def match_type(self, match_type):
        if match_type == "exhibition":
            GAME.total_overs = "1"
            SCOREBOARD.target_runs = None
        else:
            GAME.total_overs = "10"
            if match_type == "easy":
                SCOREBOARD.target_runs = random.randint(75,199)
            elif match_type == "hard":
                SCOREBOARD.target_runs = random.randint(200,250)

    def check_runs_scored():
        GAME.dr = BATSMAN.t_player_input-BOWLER.t_ball_released

        # checking the player input
        if BATSMAN.direction == BALL.direction:

            if 0 <= GAME.dr <= 400:
                GAME.runs_scored = 6
                BATSMAN.shot = "loft"

            elif 0 <= GAME.dr <= 410:
                GAME.runs_scored = "Catch-Out"
                BATSMAN.shot = "loft"

            elif 0 <= GAME.dr <= 475:
                GAME.runs_scored = 4
                BATSMAN.shot = "stroke"

            elif 0 <= GAME.dr <= 550:
                GAME.runs_scored = random.choice([1,1,1,2,2,3])
                BATSMAN.shot = "stroke"
            
            else: GAME.check_wicket()

        else: GAME.check_wicket() 
        BALL.runs_scored = GAME.runs_scored


    def check_wicket():

        if BALL.direction != "straight":

            if -220 <= GAME.dr <= 220 and BATSMAN.direction == BALL.direction:
                GAME.runs_scored = "Caught"
            else: 
                GAME.runs_scored = 0
                BALL.delivery_played = True
        
        else: 
            GAME.runs_scored = "Bowled"
            BATSMAN.shot = "stroke"


    def display_runs(runs,target):
    
        rect = pygame.Rect(screen_width/2-100,screen_height/2-125,200,250)
        pygame.draw.rect(target,"#343434",rect)
        rect = pygame.Rect(screen_width/2-100,screen_height/2-90,200,180)
        pygame.draw.rect(target,"#B22222",rect)

        # displaying text by checking the runs scored
        if runs == 0:
            TEXT().blit("DOT",target,(screen_width/2,screen_height/2-30),50,"Action_Man")
            TEXT().blit("BALL",target,(screen_width/2,screen_height/2+30),50,"Action_Man")
        
        elif runs in ["Bowled","Catch-Out","Caught"]:
            match runs:
                case "Bowled":
                    TEXT().blit("BOWLED",target,(screen_width/2,screen_height/2),50,"Action_Man")
                case "Catch-Out":
                    TEXT().blit("CATCH",target,(screen_width/2,screen_height/2-30),50,"Action_Man")
                    TEXT().blit("OUT",target,(screen_width/2,screen_height/2+30),50,"Action_Man")
                case "Caught":
                    TEXT().blit("CAUGHT",target,(screen_width/2,screen_height/2),50,"Action_Man")

        else:
            match runs:
                case 6: txt = "SIX"
                case 4: txt = "FOUR"
                case 3: txt = "TRIPLE"
                case 2: txt = "DOUBLE"
                case 1: txt = "SINGLE"
            TEXT().blit(str(runs),target,(screen_width/2,screen_height/2-20),132)
            TEXT().blit(txt,target,(screen_width/2,screen_height/2+60),50,"Action_Man")
            